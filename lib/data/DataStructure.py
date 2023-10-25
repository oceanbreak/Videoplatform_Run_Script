"""
This module defines data structures
for Videomodule sensors data"""

from lib.calculations.CoordinateCalc import convertCoordtoDM, convertCoordtoDeg
import time


class data_keywords:

    #Enums
    NAVI = "NAVI"
    DEPTH = "DEPTH"
    ALTIMETER = "ALT"
    INCLIN = "INCLIN"
    TEMP = "TEMP"
    SONAR = "SONAR"
    
    # As array:
    as_array = (NAVI, DEPTH, ALTIMETER, INCLIN, TEMP, SONAR)
    
class BaseData:

    def __init__(self):
        self.is_corrupt = False

    def setCorrupt(self):
        self.is_corrupt = True
        return self
    
    def isCorrupt(self):
        return self.is_corrupt

class CoordinatesData(BaseData):

    # Helper dict of signs of each letters
    coord_sign = {'N':1, 'S':-1, 'E':1, 'W':-1}

    def __init__(self, lat : float, lon : float):
        """
        :param input_coords: DD.DDD, DD.DDD
        :return: coords in gps format DDMM.MMMMMM, 'N'
        where D is degree, M is minute.
        """
        super().__init__()
        if type(lat) == type(lon) == float:
            self.lat = lat
            self.lon = lon
        # Handle string input
        elif type(lat) == type(lon) == str:
            try:
                deg_lat, min_lat, letter_lat = lat.split(' ')
                deg_lon, min_lon, letter_lon = lon.split(' ')
                self.lat, self.lon = convertCoordtoDeg(deg_lat, min_lat, letter_lat,
                                                       deg_lon, min_lon, letter_lon)
            except:
                print('Wrong coordinate type')
                raise ValueError
        self.pos_num = 2

    def __str__(self):
        return f'{self.lat}, {self.lon}'
    
    def log_header(self):
        return ['Lat', 'Lon']
    
    def degrees(self):
        return (self.lat, self.lon)

    def deg_min(self):
        return convertCoordtoDM(self.lat, self.lon)
    
    def toDisplayText(self):
        degr_lat, min_lat, letter_lat, degr_lon, min_lon, letter_lon = self.deg_min()
        return f"{degr_lat:.0f} {min_lat:.4f}'{letter_lat}, {degr_lon:.0f} {min_lon:.4f}'{letter_lon}"
    
    def toLogItem(self):
        degr_lat, min_lat, letter_lat, degr_lon, min_lon, letter_lon = self.deg_min()
        return f"{degr_lat:.0f} {min_lat:.4f} {letter_lat};{degr_lon:.0f} {min_lon:.4f} {letter_lon}".split(';')
        


class DepthData(BaseData):

    def __init__(self, depth : float):
        super().__init__()
        self.depth = depth
        self.pos_num = 1

    def value(self):
        return self.depth

    def __str__(self):
        return f'Depth range: {self.depth:.1f} m'
    
    def log_header(self):
        return 'm'
    
    def toDisplayText(self):
        return f'{self.depth:.1f} m'
    
    def toLogItem(self):
        return f'{self.depth:.1f}'

    
class TemperatureData(BaseData):

    def __init__(self, temp):
        super().__init__()
        self.temp = temp - 3.0
        self.pos_num = 1
        # self.keyword = data_keywords.DEPTH

    def value(self):
        return self.temp
    
    def __str__(self):
        return f'Temp: {self.temp:.1f}'
    
    def log_header(self):
        return 'C'
    
    def toDisplayText(self):
        return f'{self.temp:.1f} C'
    
    def toLogItem(self):
        return f'{self.temp:.1f}'
    

class InclinometerData(BaseData):

    def __init__(self, pitch : int, roll : int, heading : int):
        super().__init__()
        self.pitch = pitch
        self.roll = roll
        self.heading = heading
        self.pos_num = 3

    def __str__(self):
        return f'Pitch: {self.pitch}, Roll: {self.roll}, Heading: {self.heading}'
    
    def log_header(self):
        return ['Pitch', 'Roll', 'Heading']
    
    def toDisplayText(self):
        return self.__str__()
    
    def toLogItem(self):
        return f"{self.pitch:.1f};{self.roll:.1f};{self.heading:.1f}".split(";")
    

class ComPortString():
    # NMEA String or Inclinometer string with keyword

    def __init__(self, keyword, string):
        super().__init__()
        self.string = string
        self.keyword = keyword

    def __str__(self):
        return str(self.keyword) + ": " + str(self.string)
    

# Common datatype

class DateTime(BaseData):

    def __init__(self, gmtime : time.struct_time, UTC=True):
        super().__init__()
        self.year = gmtime.tm_year
        self.mon = gmtime.tm_mon
        self.day = gmtime.tm_mday
        self.hour = gmtime.tm_hour
        self.min = gmtime.tm_min
        self.sec = gmtime.tm_sec
        self.postfix = 'UTC' if UTC else ''
        self.pos_num = 2


    def log_header(self):
        return ['Date', f'Time{self.postfix}']


    def toDisplayText(self):
        return f'{self.year}/{self.mon:0>2}/{self.day:0>2}  {self.hour:0>2}:{self.min:0>2}:{self.sec:0>2} {self.postfix}'
    
    def toLogItem(self):
        return [f'{self.year}/{self.mon:0>2}/{self.day:0>2}', \
                f'{self.hour:0>2}:{self.min:0>2}:{self.sec:0>2}']


class LengthUnit(BaseData):
    # Length of track in meters

    def __init__(self, length):
        super().__init__()
        self.length = length
        self.pos_num = 1

    def log_header(self):
        return 'm'

    def toDisplayText(self):
        return f'{self.length:.1f} m'
    
    def toLogItem(self):
        return f'{self.length:.1f}'
    

class TimeUnit(BaseData):
     # Duration of track in sec

    def __init__(self, secs):
        super().__init__()
        self.secs = secs
        self.pos_num = 1

    def log_header(self):
        return ''

    def convertToHMS(self):
        self.hh = self.secs // 3600
        self.mm = self.secs // 60
        self.ss = self.secs % 60

    def toDisplayText(self):
        self.convertToHMS()
        return f'{self.hh:0>2.0f}:{self.mm:0>2.0f}:{self.ss:0>4.1f}'
    
    def toLogItem(self):
        return self.toDisplayText()