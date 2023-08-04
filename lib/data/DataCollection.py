# Data collection according to Settings

from lib.data.DataStructure import *

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
        out_string = ''
        types = (CoordinatesData, DepthData, DepthData, TemperatureData, InclinometerData)
        for var, cur_type in zip(self.var_list, types):
            if type(var) == cur_type:
                text = self.navi_data.toDisplayText()
            else:
                text = 'No data'
            out_string += f'{text}\n'
           