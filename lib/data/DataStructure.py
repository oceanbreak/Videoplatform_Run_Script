"""
This module defines data structures
for Videomodule sensors data"""

from lib.calculations.CoordinateCalc import convertCoordtoDM


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
        self.keyword = data_keywords.NAVI

    def __str__(self):
        return f'{self.lat}, {self.lon}'
    
    def degrees(self):
        return (self.lat, self.lon)

    def deg_min(self):
        return convertCoordtoDM(self.lat, self.lon)


class DepthData:

    def __init__(self, depth : float):
        self.depth = depth
        self.keyword = data_keywords.DEPTH

    def value(self):
        return self.depth

    def __str__(self):
        return f'Depth range: {self.depth:.1f} m'

    
class TemeratureData:

    def __init__(self, temp):
        self.temp = temp
        self.keyword = data_keywords.DEPTH

    def value(self):
        return self.temp
    
    def __str__(self):
        return f'Temp: {self.temp:.1f}'
    

class InclinometerData:

    def __init__(self, pitch : int, roll : int, heading : int):
        self.pitch = pitch
        self.roll = roll
        self.heading = heading
