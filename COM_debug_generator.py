"""
Module for simulating Videomodule data
for debugging purposes
"""

from lib.data.ComPortData import ComPortData
import time
import random


class NmeaComSim:

    def __init__(self):
        self.__com_port_object = None
        self.cur_message = b'No message\n\r'
        self.cur_val = 0
    
    def setPort(self, port, rate, timeout):
        self.__com_port_object = ComPortData(port, rate, timeout)

    def setInitValue(self, val):
        self.init_val = val
        self.cur_val = val

    def sendDataToPort(self):
        self.__com_port_object.sendMessage(self.cur_message)

    def closePort(self):
        self.__com_port_object.closePort()

    def generateRandFactor(self):
        factor = random.randint(-20, 20)
        self.cur_val = self.init_val + factor/10



class DepthSim(NmeaComSim):

    def __init__(self):
        super().__init__()

    def generateMessage(self):
        self.generateRandFactor()
        message = f'$--DBS,,,{self.cur_val:.1f},M,,F*hh\n\r'
        self.cur_message = bytes(message, 'utf-8')


class AltSim(NmeaComSim):

    def __init__(self):
        super().__init__()
    
    def initTempVal(self, val):
        self.temp_val = val

    def update_temp_val(self):
        self.temp_val += random.randint(-10, 10)/10

    def generateMessageDepth(self):
        self.generateRandFactor()
        message = f'$--DBT,,,{self.cur_val:.1f},M,,F*hh\n\r'
        self.cur_message = bytes(message, 'utf-8')

    def generateMessageTemp(self):
        self.update_temp_val()
        message = f'$--MTW,{self.temp_val:.1f},C*hh\n\r'
        self.cur_message = bytes(message, 'utf-8')





if __name__ == '__main__':

    try:
        sim1 = DepthSim()
        sim1.setPort('COM4', 9600, 5)
        sim1.setInitValue(128)

        sim2 = AltSim()
        sim2.setPort('COM10', 57600, 5)
        sim2.setInitValue(5)
        sim2.initTempVal(24)

        while True:
            print(time.asctime(), 'sending message')
            sim1.generateMessage()
            sim1.sendDataToPort()
            sim2.generateMessageDepth()
            sim2.sendDataToPort()
            sim2.generateMessageTemp()
            sim2.sendDataToPort()
            # message = bytes('$--DBT,,10,M,,,,*1C\n\r', 'utf-8')
            # sample_depth_data.sendMessage()
            time.sleep(1)

    finally:
        sim1.closePort()


