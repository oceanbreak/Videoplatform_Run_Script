""""
Module provides access to COM port with NMEA data and parses string with needed keyword
"""
import serial, re, operator
from functools import reduce

class ComPortData:
    def __init__(self, port_name, port_speed, port_timeout, keyword):
        self._port_name = port_name
        self._port_speed = port_speed
        self._port_timeout = port_timeout
        self._keyword = keyword
        self._line = ''
        self._word = []
        self._func_set = {'GPGGA' : self.parseGPGGA, 'SDDBT' : self.parseSDDBT}
        self._input_data = []
        self._output_data = None
        try:
            self._port = serial.Serial(self._port_name, self._port_speed, timeout = self._port_timeout)
            print('SonarCom: ' + self._port_name + ' opened successful')
            # Read all characters before new line
            temp_char = None
            while temp_char != b'\n':
                temp_char = self._port.read()
        except serial.SerialException:
            print('ERROR SonarCom: Cannot connect to port ' + self._port_name)
            exit(1)

    def readFromPort(self):
        if self._port.is_open:
            self._line = self._port.readline().decode('utf-8')
            self._line = self._line.rstrip()
            self._word = self._line.split(',')

    def pullData(self):
        wait_count = 20
        prog = re.compile('\D*' + self._keyword)
        for i in range(wait_count):
            self._data = []
            self.readFromPort()
            if prog.match(self._line):
                break
        if self.checksumOk() and i < wait_count - 1:
            self._input_data = self._word
        else:
            self._input_data = []

    def checksumOk(self):
        try:
            check_line = ','.join(self._word)[1:-3]
            checksum = '*%02X' % reduce(operator.xor, map(ord, check_line), 0)
            return checksum == self._word[-1][-3:]
        except IndexError:
            return False

    def executeParser(self):
        try:
            self._func_set[self._keyword]()
        except KeyError:
            print('ERROR SonarCom: Not valid keyword "%s"\nChoose from: '\
                  'GPGGA, GPGLL' % self._keyword)

    def getOutputData(self):
        self.executeParser()
        return self._output_data

# Now goes set of functions that sonarCom can parse
    def parseGPGGA(self):
        self.pullData()
        try:
            self._output_data = tuple(['Coordinates', self._input_data[2][:2], self._input_data[2][2:],
                                 self._input_data[3],
                                 self._input_data[4][:3], self._input_data[4][3:],
                                 self._input_data[5]])
        except IndexError:
            self._output_data = tuple(['Coordinates'] + [None for i in range(6)])

    def parseSDDBT(self):
        self.pullData()
        try:
            self._output_data = tuple(['Echo', self._input_data[3], self._input_data[4]])
        except IndexError:
            self._output_data = tuple(['Echo'] + [None for i in range(2)])

if __name__ == '__main__':
    test_line1 = ComPortData('COM5', 4800, 10, 'GPGGA')
    for i in range(10):
        print(test_line1.getOutputData())

