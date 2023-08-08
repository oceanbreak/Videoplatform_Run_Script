"""
Module to parse NMEA strings
into values"""

import numpy as np
from lib.data.DataStructure import *
from lib.calculations.CoordinateCalc import convertCoordtoDeg


class NmeaParser:

    #Gives output data proper sign
    coord_sign = {'N':1, 'S':-1, 'E':1, 'W':-1} 

    def __init__(self):
        pass
        #TODO: parse NMEA strings to data structures

    def parseByMessage(self, string : str):
        try:
            message = string.split(',')[0]
        except (TypeError, IndexError):
            print(f"Current string can nor be parsed:\n{string}")
            return None
        # Handle diffrenct parsers with different messages
        if 'GGA' in message:
            return self.parseGGA(string)
        if 'DBT' in message:
            return self.parseDBT(string)
        if 'DBS' in message:
            return self.parseDBS(string)
        if 'MTW' in message:
            return self.parseMTW(string)

    def parseGGA(self, nmea_string : str):
        """
        params: --GGA NMEA string
        return: <CoordinatesData> object
        """
        items = nmea_string.split(',')
        try:
            latval = float(items[2])
            lonval = float(items[4])
            latsign = items[3]
            lonsign = items[5]
        except ValueError:
            return None

        lat_degrees = latval//100
        lon_degrees = lonval//100
        lat_minutes = latval % 100
        lon_minutes = lonval % 100

        lattitude = self.coord_sign[latsign] * (lat_degrees + lat_minutes/60)
        longtitude = self.coord_sign[lonsign] * (lon_degrees + lon_minutes/60)

        return CoordinatesData(lattitude, longtitude)

    
    def parseDBS(self, nmea_string : str):

        items = nmea_string.split(',')

        try:
            value = float(items[3])
            return DepthData(value)
        except ValueError:
            return None
    

    def parseDBT(self, nmea_string : str):
        items = nmea_string.split(',')
        try:
            value = float(items[3])
            return DepthData(value)
        except ValueError:
            return None

    
    def parseMTW(self, nmea_string : str):
        items = nmea_string.split(',')
        try:
            value = float(items[1])
            return TemperatureData(value)
        except ValueError:
            return None      


class InclinParser:

    def __init__(self):
        self.sign = {'0':1, '1':-1}

    def parse(self, word):

        try:

            pitch_sign = self.sign[word[8]]
            pitch_val = float(word[9:12] + '.' + word[12:14])
            pitch = pitch_sign * pitch_val

            roll_sign = self.sign[word[14]]
            roll_val = float(word[15:18] + '.' +  word[18:20])
            roll = roll_sign * roll_val      

            head_sign = self.sign[word[20]]
            head_val = float(word[21:24] + '.' +  word[24:26])
            head = head_sign * head_val

            return InclinometerData(pitch, roll, head)
        
        except (IndexError, ValueError):
            return None



    

    


