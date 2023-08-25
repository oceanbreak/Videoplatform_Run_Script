""""
Module provides access to COM port with NMEA data and parses string with needed keyword
"""
import serial, re, operator
from functools import reduce
from lib.data.DataStructure import ComPortString
import time

class ComPortData:

    def __init__(self, port_name, port_speed, port_timeout, messages=[], keywords=[]):
        self._port_name = port_name
        self._port_speed = port_speed
        self._port_timeout = port_timeout
        self.__messages = messages
        self.__keywords = keywords
        self._line = ''
        self._input_data = [None] * len(self.__keywords) # Initialize array for strings to parse
        self._prev_data = [None] * len(self.__keywords)
        self.prog = [] # Initialize compile message for regexp
        self.time_out_timer = 0
        self.same_data_timestamp = [time.time()] * len(self.__keywords) # Timestamp for tracking unchanged data


        # Program regexp
        for index, message in enumerate(self.__messages):
            self.prog.append(re.compile('\D*' + message))

        # Open port for read
        try:
            self._port = serial.Serial(self._port_name, self._port_speed, timeout = self._port_timeout)
            print('SonarCom: ' + self._port_name + ' opened successful')

        except serial.SerialException:
            print('ERROR SonarCom: Cannot connect to port ' + self._port_name)
            exit(1)


    def readHex(self, length):
        # Function that reads hex and puts directly into _input_data
        self.same_data_timestamp[0] = time.time()
        ret = self._port.read(length).hex()
        self._input_data[0] = ret
        return ret


    def readFromPort(self):
        # Function reads one line from port and stores it into self_line var
        if self._port.is_open:
            try:
                self._line = self._port.readline().decode('utf-8')
                self._line = self._line.rstrip()
            except (serial.SerialException, TypeError, UnicodeDecodeError):
                print('Bad line')
                self._line = None
            # If tmeout, set timer
            if not self._line:
                self.time_out_timer = 1
            else:
                self.time_out_timer = 0

            

            


    def pullData(self, ignore_chksm=True):
        # Pulls one line from port and stores to input_data if it matches one of keyword
        self.readFromPort()
        if self._line is not  None:
            for index, prog in enumerate(self.prog):
                if prog.match(self._line) and (self.checksumOk() or ignore_chksm):
                    self._input_data[index] = self._line
                    self.same_data_timestamp[index] = time.time()

                if self.time_out_timer > 0:
                    self._input_data[index] = None


    def checksumOk(self):
        try:
            check_line = self._line[1:-3]
            checksum = '*%02X' % reduce(operator.xor, map(ord, check_line), 0)
            return checksum == self._line[-3:]
        except IndexError:
            return False


    def getOutputData(self):
        # Return as NMEAString objects
        ret = []

        # Check if data has changed
        for index in range(len(self._input_data)):
            if time.time() - self.same_data_timestamp[index] > self._port_timeout:
                self._input_data[index] = None
            # print(f'Data [{index} timer difference: {time.time() - self.same_data_timestamp[index]}]')

        for kw, string in zip(self.__keywords, self._input_data):
            ret.append(ComPortString(kw, string))
        return ret


    def sendMessage(self, message):
        self._port.write(message)


    def closePort(self):
        self._port.close()




if __name__ == '__main__':
    test_line1 = ComPortData('COM13', 9600, 10, ['GGA', 'MTW'], ['NAVI', 'TEMP'])
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


