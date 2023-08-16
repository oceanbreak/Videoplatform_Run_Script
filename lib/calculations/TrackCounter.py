"""
Module for calculating track length and time
"""

from lib.calculations.CoordinateCalc import haversine
from lib.data.DataStructure import CoordinatesData, TimeUnit, LengthUnit
import time

class TrackCounter:

    def __init__(self):
        self.track_length = 0.0
        self.__init_coord = None
        self.__cur_time = 0.0
        self.__init_time = None

    def incrementTime(self):
        self.__cur_time = time.time() - self.__init_time

    def resetTrack(self):
        self.track_length = 0.0
        self.__cur_time = 0.0
        self.__init_coord = None
        self.__init_time = None

    def initTrackTimer(self):
        if self.__init_time is None:
            self.__init_time = time.time()
        else:
            print('Timer initiated')

    def incrementTrack(self, new_coord : CoordinatesData):
        # print(new_coord.degrees)
        # print(new_coord, new_coord.is_corrupt)
        if not new_coord.is_corrupt:
            if self.__init_coord is None:
                self.__init_coord = new_coord
            else:
                delta = haversine(new_coord.degrees(), self.__init_coord.degrees())
                self.track_length += delta
                self.__init_coord = new_coord

    def getCurTrackLength(self):
        return LengthUnit(self.track_length)
    
    def getCurTrackTime(self):
        return TimeUnit(self.__cur_time)