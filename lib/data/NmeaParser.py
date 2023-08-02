import numpy as np
from lib.data.DataStructure import *
from lib.calculations.CoordinateCalc import convertCoordtoDeg


class NmeaParser:

    #Gives output data proper sign
    coord_sign = {'N':1, 'S':-1, 'E':1, 'W':-1} 

    def __init__(self):
        pass
        #TODO: parse NMEA strings to data structures

    def parseGGA(self, nmea_string : str):
        """
        params: --GGA NMEA string
        return: <CoordinatesData> object
        """
        items = nmea_string.split(',')
        latval = float(items[2])
        lonval = float(items[4])
        latsign = items[3]
        lonsign = items[5]

        lat_degrees = latval//100
        lon_degrees = lonval//100
        lat_minutes = latval % 100
        lon_minutes = lonval % 100

        lattitude = self.coord_sign[latsign] * (lat_degrees + lat_minutes/60)
        longtitude = self.coord_sign[lonsign] * (lon_degrees + lon_minutes/60)

        coord = CoordinatesData(lattitude, longtitude)

        return coord
    
    def parseDBS(self, nmea_string : str):
        items = nmea_string.split(',')
        


    

    


