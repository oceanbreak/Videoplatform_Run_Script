"""
This module defines data structures
for Videomodule sensors data"""

from lib.calculations.Course import parse_coords_from_dd_to_ddmm


class data_keywords:

    #Enums
    NAVI = 0
    DEPTH = 1
    ALTIMETER = 2
    INCLIN = 3
    TEMP = 4
    


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
    
    def getDegrees(self):
        return (self.lat, self.lon)

    def getDM(self):
        return parse_coords_from_dd_to_ddmm((self.lat, self.lon))


class DepthData:

    def __init__(self, depth):
        self.depth = depth

    def __str__(self):
        return f'{0>.2:self.depth} m'


