
import socket
import math


class RmcToTtm:
    """
    Преобразователь RMC -> TTM.

    Получает RMC по TCP, берет из него COG собственного судна,
    преобразует локальное смещение DX/DY в дальность и истинный
    пеленг и отправляет TTM по TCP.

    Система координат DX/DY:

        DY > 0  вперед
        DY < 0  назад

        DX > 0  вправо
        DX < 0  влево

    Например:

        dx=0,   dy=100  -> 100 м впереди
        dx=50,  dy=0    -> 50 м справа
        dx=-50, dy=100  -> 50 м слева и 100 м впереди
    """

    def __init__(
        self,
        gps_host="127.0.0.1",
        gps_port=10110,
        ttm_host="127.0.0.1",
        ttm_port=10111,
        dx=50.0,
        dy=100.0,
        target_number=1,
        target_name="VIRTUAL",
        target_speed=0.0,
        target_course=0.0,
    ):
        self.gps_host = gps_host
        self.gps_port = gps_port

        self.ttm_host = ttm_host
        self.ttm_port = ttm_port

        self.dx = dx
        self.dy = dy

        self.target_number = target_number
        self.target_name = target_name

        self.target_speed = target_speed
        self.target_course = target_course

        self.gps_socket = None
        self.ttm_socket = None

    # ========================================================
    # NMEA CHECKSUM
    # ========================================================

    @staticmethod
    def nmea_checksum(sentence):
        """
        Вычисляет checksum NMEA.

        sentence должен быть без '$' и без '*XX'.
        """

        checksum = 0

        for char in sentence:
            checksum ^= ord(char)

        return f"{checksum:02X}"

    @classmethod
    def make_nmea(cls, sentence):
        """
        Добавляет '$', checksum и CR/LF.
        """

        checksum = cls.nmea_checksum(sentence)

        return f"${sentence}*{checksum}\r\n"

    # ========================================================
    # RMC
    # ========================================================

    @staticmethod
    def parse_rmc(line):
        """
        Разбирает GPRMC / GNRMC и возвращает COG.

        Если строка не является корректным RMC,
        возвращает None.
        """

        line = line.strip()

        if not line.startswith("$"):
            return None

        # Убираем checksum
        body = line.split("*", 1)[0]

        fields = body.split(",")

        if len(fields) < 9:
            return None

        # GPRMC, GNRMC, GLRMC и т.п.
        if not fields[0].endswith("RMC"):
            return None

        # A = valid
        if fields[2] != "A":
            return None

        try:
            cog = float(fields[8])
        except ValueError:
            return None

        return cog

    # ========================================================
    # DX/DY -> RANGE/BEARING
    # ========================================================

    @staticmethod
    def calculate_target(dx, dy, own_course):
        """
        Преобразует локальное смещение DX/DY
        в дальность и истинный пеленг.

        dx = вправо/влево
        dy = вперед/назад

        own_course = истинный курс собственного судна.
        """

        distance_m = math.hypot(dx, dy)

        # 0° = прямо вперед
        # +90° = справа
        # -90° = слева
        relative_bearing = math.degrees(
            math.atan2(dx, dy)
        )

        true_bearing = (
            own_course + relative_bearing
        ) % 360.0

        return distance_m, true_bearing

    # ========================================================
    # TTM
    # ========================================================

    def make_ttm(
        self,
        distance_m,
        bearing,
    ):
        """
        Формирует NMEA TTM.
        """

        # TTM использует морские мили
        distance_nm = distance_m / 1852.0

        body = (
            f"RATTM,"
            f"{self.target_number:02d},"
            f"{distance_nm:.3f},"
            f"{bearing:.1f},"
            f"T,"
            f"{self.target_speed:.1f},"
            f"{self.target_course:.1f},"
            f"T,"
            f","
            f","
            f","
            f"{self.target_name},"
            f"T,"
            f"R"
        )

        return self.make_nmea(body)

    # ========================================================
    # CONNECTIONS
    # ========================================================

    def connect_gps(self):
        """
        Подключается к TCP источнику NMEA.
        """

        print(
            f"Connecting to GPS "
            f"{self.gps_host}:{self.gps_port}"
        )

        self.gps_socket = socket.create_connection(
            (
                self.gps_host,
                self.gps_port
            )
        )

        print("GPS connected.")

    def start_ttm_server(self):
        """
        Запускает TCP server для OpenCPN.
        """

        server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        server.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1
        )

        server.bind(
            (
                self.ttm_host,
                self.ttm_port
            )
        )

        server.listen(1)

        print(
            f"Waiting for OpenCPN on "
            f"{self.ttm_host}:{self.ttm_port}"
        )

        self.ttm_socket, address = server.accept()

        print(
            f"OpenCPN connected from {address}"
        )

        # После accept серверный сокет больше не нужен.
        server.close()

    # ========================================================
    # PROCESSING
    # ========================================================

    def process_rmc(self, line):
        """
        Обрабатывает одну строку NMEA.

        Если это RMC, формирует TTM и отправляет его.

        Возвращает созданный TTM или None.
        """

        course = self.parse_rmc(line)

        if course is None:
            return None

        distance_m, bearing = self.calculate_target(
            self.dx,
            self.dy,
            course
        )

        ttm = self.make_ttm(
            distance_m,
            bearing
        )

        self.ttm_socket.sendall(
            ttm.encode("ascii")
        )

        return ttm

    # ========================================================
    # MAIN LOOP
    # ========================================================

    def run(self):
        """
        Основной цикл.

        Читает NMEA от GPS и отправляет TTM.
        """

        self.connect_gps()
        self.start_ttm_server()

        buffer = ""

        while True:

            data = self.gps_socket.recv(4096)

            if not data:
                print("GPS disconnected.")
                break

            buffer += data.decode(
                "ascii",
                errors="ignore"
            )

            while "\n" in buffer:

                line, buffer = buffer.split(
                    "\n",
                    1
                )

                line = line.strip()

                ttm = self.process_rmc(line)

                if ttm is None:
                    continue

                course = self.parse_rmc(line)

                distance_m, bearing = (
                    self.calculate_target(
                        self.dx,
                        self.dy,
                        course
                    )
                )

                print(
                    f"COG={course:6.1f}°  "
                    f"DX={self.dx:7.1f} m  "
                    f"DY={self.dy:7.1f} m  "
                    f"Range={distance_m:7.1f} m  "
                    f"Bearing={bearing:6.1f}°"
                )

                print(
                    f"  {ttm.strip()}"
                )

    # ========================================================
    # CLOSE
    # ========================================================

    def close(self):
        """
        Закрывает соединения.
        """

        if self.gps_socket is not None:
            self.gps_socket.close()

        if self.ttm_socket is not None:
            self.ttm_socket.close()




def main():

    converter = RmcToTtm(
        gps_host="127.0.0.1",
        gps_port=3100,

        ttm_host="127.0.0.1",
        ttm_port=10111,

        dx=50.0,
        dy=100.0,

        target_number=1,
        target_name="VIRTUAL",

        target_speed=0.0,
        target_course=0.0,
    )

    try:
        converter.run()

    except KeyboardInterrupt:
        print("\nStopping...")

    finally:
        converter.close()


if __name__ == "__main__":
    main()
