"""
This module defines data structures
for Videomodule sensors data"""

from lib.calculations.CoordinateCalc import convertCoordtoDM
import time


class data_keywords:

    #Enums
    NAVI = "NAVI"
    DEPTH = "DEPTH"
    ALTIMETER = "ALT"
    INCLIN = "INCLIN"
    TEMP = "TEMP"
    
    # As array:
    as_array = (NAVI, DEPTH, ALTIMETER, INCLIN, TEMP)
    


class CoordinatesData:

    # Helper dict of signs of each letters
    coord_sign = {'N':1, 'S':-1, 'E':1, 'W':-1}

    def __init__(self, lat : float, lon : float):
        """
        :param input_coords: DD.DDD, DD.DDD
        :return: coords in gps format DDMM.MMMMMM, 'N'
        where D is degree, M is minute.
        """
        self.lat = lat
        self.lon = lon
        self.keyword = None

    def __str__(self):
        return f'{self.lat}, {self.lon}'
    
    def degrees(self):
        return (self.lat, self.lon)

    def deg_min(self):
        return convertCoordtoDM(self.lat, self.lon)
    
    def toDisplayText(self):
        degr_lat, min_lat, letter_lat, degr_lon, min_lon, letter_lon = self.deg_min()
        return f"{degr_lat:.0f} {min_lat:.3f}'{letter_lat}, {degr_lon:.0f} {min_lat:.3f}'{letter_lon}"
    
    def toLogItem(self):
        degr_lat, min_lat, letter_lat, degr_lon, min_lon, letter_lon = self.deg_min()
        return f"{degr_lat:.0f};{min_lat:.3f};{letter_lat};{degr_lon:.0f};{min_lat:.3f};{letter_lon}".split(';')
        


class DepthData:

    def __init__(self, depth : float):
        self.depth = depth
        self.keyword = None

    def value(self):
        return self.depth

    def __str__(self):
        return f'Depth range: {self.depth:.1f} m'
    
    def toDisplayText(self):
        return f'{self.depth:.1f} m'
    
    def toLogItem(self):
        return f'{self.depth:.1f}'

    
class TemperatureData:

    def __init__(self, temp):
        self.temp = temp
        # self.keyword = data_keywords.DEPTH

    def value(self):
        return self.temp
    
    def __str__(self):
        return f'Temp: {self.temp:.1f}'
    
    def toDisplayText(self):
        return f'{self.temp:.1f} C'
    
    def toLogItem(self):
        return f'{self.temp:.1f}'
    

class InclinometerData:

    def __init__(self, pitch : int, roll : int, heading : int):
        self.pitch = pitch
        self.roll = roll
        self.heading = heading
        self.kewword = None

    def __str__(self):
        return f'Pitch: {self.pitch}, Roll: {self.roll}, Heading: {self.heading}'
    
    def toDisplayText(self):
        return self.__str__()
    
    def toLogItem(self):
        return self.pitch, self.roll, self.heading
    

class ComPortString:
    # NMEA String or Inclinometer string with keyword

    def __init__(self, keyword, string):
        self.keyword = keyword
        self.string = string

    def __str__(self):
        return str(self.keyword) + ": " + str(self.string)
    

# Common datatype

class DateTime:

    def __init__(self, gmtime : time.struct_time):
        self.year = gmtime.tm_year
        self.mon = gmtime.tm_mon
        self.day = gmtime.tm_mday
        self.hour = gmtime.tm_hour
        self.min = gmtime.tm_min
        self.sec = gmtime.tm_sec

    def toDisplayText(self):
        return f'{self.year}/{self.mon:0>2}/{self.day:0>2}  {self.hour:0>2}:{self.min:0>2}:{self.sec:0>2} UTC'
    
    def toLogItem(self):
        return [f'{self.year}/{self.mon:0>2}/{self.day:0>2}', \
                f'{self.hour:0>2}:{self.min:0>2}:{self.sec:0>2}']


class LengthUnit:
    # Length of track in meters

    def __init__(self, length):
        self.length = length

    def toDisplayText(self):
        return f'{self.length:.1f} m'
    
    def toLogItem(self):
        return f'{self.length:.1f}'
    

class TimeUnit:
     # Duration of track in sec

    def __init__(self, secs):
        self.secs = secs

    def convertToHMS(self):
        self.hh = self.secs // 3600
        self.mm = self.secs // 60
        self.ss = self.secs % 60

    def toDisplayText(self):
        self.convertToHMS()
        return f'{self.hh:0>2.0f}:{self.mm:0>2.0f}:{self.ss:0>2.0f}'
    
    def toLogItem(self):
        return self.toDisplayText()