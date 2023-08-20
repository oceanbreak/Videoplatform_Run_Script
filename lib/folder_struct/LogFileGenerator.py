"""
Module to write log file
"""
from lib.data.DataCollection import DataCollection
import os
import time

class LogFileGeneraror:

    def __init__(self, file_path : str, data_collection : DataCollection):
        self.path = file_path
        self.data_collection = data_collection
        self.file_name = self.generateFileName()
        self.file_full_path = os.path.join(self.path, self.file_name)
        
        # Write header
        with open(self.file_full_path, 'a') as fs:
            to_write = [item if item!=None else '' for item in self.data_collection.logHeader()]
            fs.write(';'.join(to_write))
            fs.write('\n')


    def writeLogString(self):
        with open(self.file_full_path, 'a') as fs:
            to_write = [item if item!=None else '' for item in self.data_collection.toLogItemsList()]
            fs.write(';'.join(to_write))
            fs.write('\n')


    def generateFileName(self, prefix = 'log', extension = 'csv'):
        cur_time = self.data_collection.datetime.data
        # date_str = '{:0>4}'.format(cur_time.tm_year) +  '{:0>2}'.format(cur_time.tm_mon)  + '{:0>2}'.format(cur_time.tm_mday)[-2:]
        # time_str = '{:0>2}'.format(cur_time.tm_hour) + '{:0>2}'.format(cur_time.tm_min)  + '{:0>2}'.format(cur_time.tm_sec)
        datetime_str = f'{cur_time.year}{cur_time.mon:0>2}{cur_time.day:0>2}_{cur_time.hour:0>2}{cur_time.min:0>2}{cur_time.sec:0>2}'
        return prefix + '_' + datetime_str + '.' + extension
