"""
This module sets 10 m level and resets zero at surface for depth sensor
"""

import serial

class SonarDepth:
    def __init__(self, depth_port, depth_rate):
        self._depth_port = depth_port
        self._depth_rate = depth_rate
        self._flag = True
        try:
            self._port = serial.Serial(depth_port, depth_rate, timeout=None)
            self._port.close()
        except serial.SerialException:
            print("ERROR sonar_set_depth:  NO ACCESS TO PORT")
            self._flag = False

    def set_depth(self):
        if self._flag:
            self._port.open()
            self._port.write('set 10')
            print("===== 10m SET =====")
            self._port.close()

    def reset_depth(self):
        if self._flag:
            self._port.open()
            self._port.write('reset')
            print("===== ZERO RESET =====")
            self._port.close()

if __name__ == '__main__':
    test1 = SonarDepth('COM4', 9600)
    test1.set_depth()
    test1.reset_depth()