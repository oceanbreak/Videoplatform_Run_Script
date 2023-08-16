# Data collection according to Settings
# It stores datain memeory for access of defferent parts of the program

from lib.data.DataStructure import *
from lib.UI.Settings import ComPortSettings, Settings
from lib.data.NmeaParser import NmeaParser, InclinParser
from lib.data.DataStructure import BaseData

class DataPacket:
    """
    Data packet for chanels that has a flag that data is corrupted
    """

    def __init__(self,  data : BaseData, enable=True):

        # Flags that show if data availible
        self.__corrupt = False
        self.__enable = enable

        # Info about data 
        self.data = data

        # Set corrupt is None or empty line came
        if data.is_corrupt: self.set_corrupt()

    def enable(self):
        self.__enable = True

    def disable(self):
        self.__enable = False

    def is_enabled(self):
        return self.__enable

    def set_corrupt(self):
        self.__corrupt = True
        return self

    def set_OK(self):
        self.__corrupt = False

    def is_corrupted(self):
        return self.__corrupt
    
    def __str__(self):
        return "Packet: " + str(self.data)

class DataCollection:

    header_TR_LENGTH = 'Tr_length'
    header_TR_TIME = 'Tr_time'
    header_NAVI = 'Nav'
    header_DEPTH = 'Depth'
    header_ALTIMETER = 'Alt'
    header_SHIP_SONAR = 'Sonar'
    header_DATE_TIME = ''
    header_TEMPERATURE = 'Temp'
    header_INCLIN = 'Incl'

    def __init__(self, settings : Settings):

        self.settings = settings
        self.clear()
        

    def clear(self):

        # Init all data as disabled except track length
        self.navi_data = DataPacket(CoordinatesData(0.0, 0.0).setCorrupt(), enable=self.settings.navi_port.is_enabled())
        self.depth_data = DataPacket(DepthData(0.0).setCorrupt(), enable=self.settings.depth_port.is_enabled())
        self.altimeter_data = DataPacket(DepthData(0.0).setCorrupt(), enable=self.settings.altimeter_port.is_enabled())
        self.temperature_data = DataPacket(TemperatureData(0.0).setCorrupt(), enable=self.settings.temp_port.is_enabled())
        self.inclinometer_data = DataPacket(InclinometerData(0.,0,0).setCorrupt(), enable=self.settings.inclin_port.is_enabled())
        self.datetime = DataPacket(DateTime(time.gmtime()).setCorrupt(), enable=False)
        self.track_length = DataPacket(LengthUnit(0.0))
        self.track_time_length = DataPacket(TimeUnit(0.0))
        self.ship_sonar_data = DataPacket(DepthData(0.0).setCorrupt(), enable=self.settings.sonar_port.is_enabled())



    def readDataFromBuffer(self, bufferRawData : dict):

        parser = NmeaParser()
        # BOOM! - time stamp
        if self.settings.UTC_time:
            self.datetime = DataPacket(DateTime(time.gmtime(), UTC=True))
        else:
            self.datetime = DataPacket(DateTime(time.localtime(), UTC=False))

        for keyword in bufferRawData:

            if keyword == data_keywords.INCLIN:
                parser_in = InclinParser()
                data = parser_in.parse(bufferRawData[keyword])
                self.inclinometer_data = DataPacket(data)

            if keyword == data_keywords.NAVI:
                message = self.settings.navi_port.message
                data = parser.parseByMessage(bufferRawData[keyword], message)
                self.navi_data = DataPacket(data)

            if keyword == data_keywords.DEPTH:
                message = self.settings.depth_port.message
                data = parser.parseByMessage(bufferRawData[keyword], message)
                self.depth_data = DataPacket(data)

            if keyword == data_keywords.ALTIMETER:
                message = self.settings.altimeter_port.message
                data = parser.parseByMessage(bufferRawData[keyword], message)
                self.altimeter_data = DataPacket(data)

            if keyword == data_keywords.TEMP:
                message = self.settings.temp_port.message
                data = parser.parseByMessage(bufferRawData[keyword], message)
                self.temperature_data = DataPacket(data)

            if keyword == data_keywords.SONAR:
                message = self.settings.sonar_port.message
                data = parser.parseByMessage(bufferRawData[keyword], message)
                self.ship_sonar_data = DataPacket(data)


    def toDisplayText(self):
        # Form textd that will be shown on display of program
        out_string = ''
        
        var_list = [self.navi_data,
                        self.depth_data,
                        self.altimeter_data,
                        self.temperature_data,
                        self.ship_sonar_data,
                        self.inclinometer_data,
                        self.datetime,
                        self.track_length,
                        self.track_time_length]
        
        name_list = ['', 'Depth: ', 'Alt: ', 'Temp: ', 'Sonar: ', 'Inclin: ', '', 'Track lentgh: ', 'Time elapsed: ']
        
        for var, name in zip(var_list, name_list):
            
            text = name
            if var.is_enabled():
                
                if var.is_corrupted():
                    # print('Corrupted')
                    text +=  'Data missing'
                else:
                    # print(var.data.toDisplayText())
                    text += var.data.toDisplayText()
                out_string += text + '\n'
        return out_string
    

    def toLogItemsList(self):

        var_list = [self.track_length,
                        self.navi_data,
                        self.depth_data,
                        self.altimeter_data,
                        self.datetime,
                        self.track_time_length,
                        self.temperature_data,
                        self.inclinometer_data,
                        self.ship_sonar_data]

        positions_in_list = [var.data.pos_num for var in var_list]

        output_string = []
        for var, pos_num in zip(var_list, positions_in_list):
            if var.is_enabled():
                
                if var.is_corrupted():
                    # print('Corrupted')
                    output_string += [None] * pos_num
                else:
                    to_add = var.data.toLogItem()
                    if type(to_add) == list:
                        output_string += to_add
                    else:
                        output_string.append(to_add)
            # else:
            #     # Var is None, leave places
            #     output_string += [None] * pos_num

        return output_string

    def logHeader(self):

        var_list = [self.track_length,
                        self.navi_data,
                        self.depth_data,
                        self.altimeter_data,
                        self.datetime,
                        self.track_time_length,
                        self.temperature_data,
                        self.inclinometer_data,
                        self.ship_sonar_data]
        
        # names_list = ['Tr_length', 'Nav', 'Depth', 'Alt', '', 'Tr_time', 'Temp', 'Incl']
        names_list = [self.header_TR_LENGTH,
                      self.header_NAVI,
                      self.header_DEPTH,
                      self.header_ALTIMETER,
                      self.header_DATE_TIME,
                      self.header_TR_TIME,
                      self.header_TEMPERATURE,
                      self.header_INCLIN,
                      self.header_SHIP_SONAR]

        output_string = []
        for var, header_item in zip(var_list, names_list):
            if var.is_enabled():
                var_subheader = var.data.log_header()
                if type(var_subheader) == list:
                    for word in var_subheader:
                        output_string.append(f'{header_item} {word}'.strip())
                else:
                    output_string.append(f'{header_item} {var_subheader}'.strip())

        return output_string