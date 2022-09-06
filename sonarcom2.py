""""
Module provides access to COM port with NMEA data and parses string with needed keyword
"""
import serial, re, operator
from functools import reduce

class ComPortData:
    def __init__(self, port_name, port_speed, port_timeout, keywords):
        self._port_name = port_name
        self._port_speed = port_speed
        self._port_timeout = port_timeout
        self._keywords = keywords
        self._line = ''
        self._input_data = [None] * len(self._keywords) # Initialize array for strings to parse
        self.prog = [] # Initialize compile message for regexp
        self.time_out_timer = 0

        # Program regexp
        for index, keyword in enumerate(self._keywords):
            self.prog.append(re.compile('\D*' + keyword))

        # Open port for read
        try:
            self._port = serial.Serial(self._port_name, self._port_speed, timeout = self._port_timeout)
            print('SonarCom: ' + self._port_name + ' opened successful')
            # Read all characters before new line
            # temp_char = None
            # while temp_char != b'\n':
            #     temp_char = self._port.read()
        except serial.SerialException:
            print('ERROR SonarCom: Cannot connect to port ' + self._port_name)
            exit(1)


    def readFromPort(self):
        # Function reads one line from port and stores it into self_line var
        if self._port.is_open:
            self._line = self._port.readline().decode('utf-8')
            self._line = self._line.rstrip()
            if self._line == '':
                self.time_out_timer += 1
            else:
                self.time_out_timer = 0


    def pullData(self):
        # Pulls one line from port and stores to input_data if it matches one of keyword
        self.readFromPort()
        for index, prog in enumerate(self.prog):
            if prog.match(self._line) and self.checksumOk():
                self._input_data[index] = self._line


    def checksumOk(self):
        try:
            check_line = self._line[1:-3]
            checksum = '*%02X' % reduce(operator.xor, map(ord, check_line), 0)
            return checksum == self._line[-3:]
        except IndexError:
            return False

    def getOutputData(self):
        return self._input_data

    def sendMessage(self, message):
        self._port.write(message)

    def closePort(self):
        self._port.close()


if __name__ == '__main__':
    test_line1 = ComPortData('COM12', 9600, 10, ['GGA', 'MTW'])
    output_data = [None, None]
    for i in range(1000):
        test_line1.pullData()
        data = test_line1.getOutputData()
        can_print = False
        for i, value in  enumerate(data):
            if value != output_data[i]:
                output_data[i] = value
                can_print = True
        if can_print:
            print(output_data)
    test_line1.closePort()


