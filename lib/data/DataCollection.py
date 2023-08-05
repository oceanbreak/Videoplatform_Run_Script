# Data collection according to Settings
# It stores datain memeory for access of defferent parts of the program

from lib.data.DataStructure import *
from lib.folder_struct.Settings import ComPortSettings

class ChannelDataPacket:
    """
    Data pachet for COM Port channels
    that stores info about COM port settings and data
    """

    def __init__(self, source : ComPortSettings, data):

        # Flags that show if data availible
        self.__corrupt = False

        # Info about source of data and data intself
        self.source = source
        self.data = data

    def set_corrupt(self):
        self.__corrupt = True

    def set_OK(self):
        self.__corrupt = False

    def is_corrupted(self):
        return self.__corrupt

class DataCollection:

    def __init__(self):

        self.navi_data = None
        self.depth_data = None
        self.altimeter_data = None
        self.temperature_data = None
        self.inclinometer_data = None
        self.datetime = None
        self.track_length = None
        self.track_time_length = None

        self.var_list = (self.navi_data,
                        self.depth_data,
                        self.altimeter_data,
                        self.temperature_data,
                        self.inclinometer_data,
                        self.datetime,
                        self.track_length,
                        self.track_time_length)

    def toDisplayText(self):
        # Form textd that will be shown on display of program
        out_string = ''
        for var in self.var_list:
            if var is not None:
                if var.is_corrupted:
                    text = 'Data missing'
                else:
                    text = var.data.toDisplayText()
        out_string += text + '\n'


    def toLogFileLine(self):
        pass
