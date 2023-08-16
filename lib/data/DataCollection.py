# Data collection according to Settings
# It stores datain memeory for access of defferent parts of the program

from lib.data.DataStructure import *
from lib.UI.Settings import ComPortSettings
from lib.data.NmeaParser import NmeaParser, InclinParser

class DataPacket:
    """
    Data packet for chanels that has a flag that data is corrupted
    """

    def __init__(self,  data, enable=True):

        # Flags that show if data availible
        self.__corrupt = False
        self.__enable = enable

        # Info about data 
        self.data = data

        # Set corrupt is None or empty line came
        if data is None: self.set_corrupt()

    def enable(self):
        self.__enable = True

    def disable(self):
        self.__enable = False

    def is_enabled(self):
        return self.__enable

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

        self.navi_data = DataPacket(CoordinatesData(0.0, 0.0), enable=False)
        self.depth_data = DataPacket(DepthData(0.0), enable=False)
        self.altimeter_data = DataPacket(DepthData(0.0), enable=False)
        self.temperature_data = DataPacket(TemperatureData(0.0), enable=False)
        self.inclinometer_data = DataPacket(InclinometerData(0.,0,0), enable=False)
        self.datetime = None
        self.track_length = DataPacket(LengthUnit(0.0))
        self.track_time_length = DataPacket(TimeUnit(0.0))


    def clear(self):
        self.__init__()



    def readDataFromBuffer(self, bufferRawData : dict):

        parser = NmeaParser()
        # BOOM! - time stamp
        self.datetime = DataPacket(DateTime(time.localtime(), UTC=False))

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
    

    def toLogItemsList(self):

        var_list = [self.track_length,
                        self.navi_data,
                        self.depth_data,
                        self.altimeter_data,
                        self.datetime,
                        self.track_time_length,
                        self.temperature_data,
                        self.inclinometer_data]
        
        # positions_in_list = [1, 6, 1, 1, 2, 1, 1, 3]
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
            else:
                # Var is None, leave places
                output_string += [None] * pos_num

        return output_string

    def logHeader(self):

        var_list = [self.track_length,
                        self.navi_data,
                        self.depth_data,
                        self.altimeter_data,
                        self.datetime,
                        self.track_time_length,
                        self.temperature_data,
                        self.inclinometer_data]
        
        positions_in_list = [1, 6, 1, 1, 2, 1, 1, 3]

        output_string = []
        for var, pos_num in zip(var_list, positions_in_list):
            if var is not None:
                
                if var.is_corrupted():
                    # print('Corrupted')
                    output_string += [None] * pos_num
                else:
                    to_add = var.data.toLogItem()
                    if type(to_add) == list:
                        output_string += to_add
                    else:
                        output_string.append(to_add)
            else:
                # Var is None, leave places
                output_string += [None] * pos_num

        return output_string