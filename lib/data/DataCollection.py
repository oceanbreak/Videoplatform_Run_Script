# Data collection according to Settings
# It stores datain memeory for access of defferent parts of the program

from lib.data.DataStructure import *
from lib.UI.Settings import ComPortSettings
from lib.data.NmeaParser import NmeaParser, InclinParser

class DataPacket:
    """
    Data packet for chanels that has a flag that data is corrupted
    """

    def __init__(self,  data):

        # Flags that show if data availible
        self.__corrupt = False

        # Info about data 
        self.data = data

        # Set corrupt is None or empty line came
        if data is None: self.set_corrupt()

    def set_corrupt(self):
        self.__corrupt = True

    def set_OK(self):
        self.__corrupt = False

    def is_corrupted(self):
        return self.__corrupt
    
    def __str__(self):
        return "Packet: " + str(self.data)

class DataCollection:

    def __init__(self):

        self.navi_data = None
        self.depth_data = None
        self.altimeter_data = None
        self.temperature_data = None
        self.inclinometer_data = None
        self.datetime = None
        self.track_length = DataPacket(LengthUnit(0.0))
        self.track_time_length = DataPacket(TimeUnit(0.0))



    def readDataFromBuffer(self, bufferRawData : dict):

        parser = NmeaParser()
        # BOOM! - time stamp
        self.datetime = DataPacket(DateTime(time.gmtime()))

        for keyword in bufferRawData:

            if keyword == data_keywords.INCLIN:
                parser_in = InclinParser()
                data = parser_in.parse(bufferRawData[keyword])
                self.inclinometer_data = DataPacket(data)

            if keyword == data_keywords.NAVI:
                data = parser.parseByMessage(bufferRawData[keyword])
                self.navi_data = DataPacket(data)

            if keyword == data_keywords.DEPTH:
                data = parser.parseByMessage(bufferRawData[keyword])
                self.depth_data = DataPacket(data)

            if keyword == data_keywords.ALTIMETER:
                data = parser.parseByMessage(bufferRawData[keyword])
                self.altimeter_data = DataPacket(data)

            if keyword == data_keywords.TEMP:
                data = parser.parseByMessage(bufferRawData[keyword])
                self.temperature_data = DataPacket(data)



    def toDisplayText(self):
        # Form textd that will be shown on display of program
        out_string = ''
        
        var_list = [self.navi_data,
                        self.depth_data,
                        self.altimeter_data,
                        self.temperature_data,
                        self.inclinometer_data,
                        self.datetime,
                        self.track_length,
                        self.track_time_length]
        
        name_list = ['', 'Depth: ', 'Alt: ', 'Temp: ', 'Inclin: ', '', 'Track lentgh: ', 'Time elapsed: ']
        
        for var, name in zip(var_list, name_list):
            
            text = name
            if var is not None:
                
                if var.is_corrupted():
                    # print('Corrupted')
                    text +=  'Data missing'
                else:
                    # print(var.data.toDisplayText())
                    text += var.data.toDisplayText()
                out_string += text + '\n'
        return out_string


    def toLogFileLine(self):
        pass
