"""
This module generates srt file for video
based of known log file for Videomodule
with video name containing start and end time
"""

import os
from tkinter import filedialog
from lib.UI.Settings import Settings
from lib.data.DataCollection import DataCollection
from lib.data.DataStructure import *

class LogVariable:
    """
    Custom class for variable to access it through list
    """

    def __init__(self):
        self.value = False



class LogString:
    """
    Class for storing log string data
    """

    def __init__(self, log_header : list, log_string : list, log_mapper : list):

        self.log_header = log_header
        self.log_string = log_string
        self.log_mapper = log_mapper

        self.date = LogVariable()
        self.time = LogVariable()
        self.track_length = LogVariable()
        self.track_time = LogVariable()
        self.nav_lat = LogVariable()
        self.nav_lon = LogVariable()
        self.depth = LogVariable()
        self.altimeter = LogVariable()
        self.sonar = LogVariable()
        self.temp = LogVariable()
        self.inc_pitch = LogVariable()
        self.inc_roll = LogVariable()
        self.inc_head = LogVariable()

        self.map_vars = (self.date,
                         self.time,
                         self.track_length,
                         self.track_time,
                         self.nav_lat,
                         self.nav_lon,
                         self.depth,
                         self.altimeter,
                         self.sonar,
                         self.temp,
                         self.inc_pitch,
                         self.inc_roll,
                         self.inc_head)
        
        self.getFromLogString()


    def getFromLogString(self):
        for name, val in zip(self.log_header, self.log_string):
            for map_name in self.log_mapper:
                if name in map_name:
                    index = self.log_mapper.index(map_name)
                    self.map_vars[index].value = val

                    break

    def toSrtString(self):
        # Make SRT string based on what is availible

        # NAVI
        if self.nav_lat.value and self.nav_lon.value:
            navigation_string = self.nav_lat.value + ' ' + self.nav_lon.value + '\n'
        else:
            navigation_string = ''

        # DEPTH, ALT
        dep_alt_string = ''
        if self.depth.value:
            dep_alt_string += f'Depth: {self.depth.value} m'
        if self.altimeter.value:
            dep_alt_string += f', Alt: {self.altimeter.value} m'
        if len(dep_alt_string) > 0:
            dep_alt_string += '\n'

        # Sonar, temperature
        sonar_temp_string = ''
        if self.sonar.value:
            sonar_temp_string += f'Sonar: {self.sonar.value} m'
        if self.temp.value:
            sonar_temp_string += f', Temp: {self.temp.value} C'
        if len(sonar_temp_string) > 0:
            sonar_temp_string += '\n'

        # Inclinometer
        if self.inc_head.value and self.inc_pitch.value and self.inc_roll.value:
            incl_string = f'Pitch: {self.inc_pitch.value}, Roll: {self.inc_roll.value}, Heading: {self.inc_head.value}\n'
        else:
            incl_string = ''


        # DateTime
        date_time_string = f'{self.date.value} {self.time.value}\n'

        # Track length string
        tr_length_string = f'Track length: {self.track_length.value}, time elapsed: {self.track_time.value}'

        return navigation_string + dep_alt_string + sonar_temp_string + incl_string + \
                    date_time_string + tr_length_string
        

class LogReader:
    
    # Class that stores data read from log-file
    # based on its header

    def __init__(self, log_file_path, data_collection : DataCollection):
        self.data_collection = data_collection
        self.log_file_path = log_file_path
        
        self.map_header = data_collection.logHeader(ignore_enabled=True)
        self.header = None
        # print(self.full_header)

        self.log_data = {}


    def readLogHeader(self):
        # Read header
        # :return list of data types with column numbers

        with open(self.log_file_path, 'r') as log:
            header_string = log.readline().rstrip().split(';')

        return header_string
    
    def readLogFile(self):
        i=0
        with open(self.log_file_path, 'r') as log:
            for line in log:
                if i==0:
                    self.header = self.readLogHeader()
                else:
                    line = line.rstrip().split(';')
                    log_line = LogString(self.header, line, self.map_header)

                    self.log_data[(log_line.date, log_line.time)] = log_line

                i+=1


    # def readLogFile(self):
    #     """
    #     Takes log file and splits it into dictionary
    #     where key is real time and value is other data
    #     :param path:
    #     :return:
    #     """
    #     log = {}
    #     for log_file in self.log_list:
    #         with open(os.path.join(path, log_file), 'r') as log_input:
    #             for line in log_input:
    #                 data = line.rstrip().split(';')
    #                 date_time = '_'.join(data[-2:])
    #                 log[date_time] = data[:-2]
    #     return log


class SrtFromLog:

    video_format_list = ['avi', 'AVI', 'mp4', 'MP4']

    def __init__(self, settings : Settings, data_collection : DataCollection):
        self.data_collection = data_collection
        self.settings = settings
        self.folder_path = None
        self.log_list = [name for name in os.listdir(self.log_file_path) if name.split('.')[-1] == 'csv']

    def askFolder(self):
        ret = filedialog.askdirectory(initialdir=self.settings.default_folder)
        if ret != '':
            self.folder_path = ret

    def getVideoList(self):
        self.video_list = [name for name in os.listdir(self.folder_path) 
                           if name.split('.')[-1] in self.video_format_list
                            and name[0]=='R']


# Utils functions
def timeToSec(hhmmss_string):
    hh, mm, ss = map(int, hhmmss_string.split(':'))
    return hh * 3600 + mm * 60 + ss


def secToTime(srt_timer):
    # converts number into srt time format
    return '{:0>2}'.format(srt_timer//3600) + ':' \
           + '{:0>2}'.format((srt_timer//60) % 60) + ':' \
           + '{:0>2}'.format(srt_timer % 60)

def log_string_format(log_string):
    return ' '.join(log_string[1:7]) + \
            '\nDistance: %s m\nDepth: %s m Altimeter: %s m' % (log_string[0], log_string[7], log_string[9])


def getVideoList(path):
    video_list = [name for name in os.listdir(path) if name.split('.')[-1] == 'avi'
                  and name[0]=='R']
    return video_list


def getStartEndTime(video_name):
    """
    This function takes video name and generates timecode relation
    between video time and real time from log file
    :param video_name:
    :return: dictionary that maps real time to video timecode
    """
    start_date = video_name.split('_')[1]
    start_date = "/".join([start_date[6:], start_date[4:6], start_date[:4]])
    start_time = video_name.split('_')[2]
    start_time = ":".join([start_time[:2], start_time[2:4], start_time[4:]])
    end_date = video_name.split('_')[3]
    end_date = "/".join([end_date[6:], end_date[4:6], end_date[:4]])
    end_time = video_name.split('_')[4].split('.')[0]
    end_time = ":".join([end_time[:2], end_time[2:4], end_time[4:]])

    video_timecode = {}
    video_length = timeToSec(end_time) - timeToSec(start_time)
    for cur_sec in range(video_length):
        cur_key = start_date + '_' + secToTime(timeToSec(start_time) + cur_sec - SEC_SRT_OFFSET)
        video_timecode[cur_key] = cur_sec

    return video_timecode


def readLogFile(path):
    """
    Takes log file and splits it into dictionary
    where key is real time and value is other data
    :param path:
    :return:
    """
    log_list = [name for name in os.listdir(path) if name.split('.')[-1] == 'csv']
    log = {}
    for log_file in log_list:
        with open(os.path.join(path, log_file), 'r') as log_input:
            for line in log_input:
                data = line.rstrip().split(';')
                date_time = '_'.join(data[-2:])
                log[date_time] = data[:-2]
    return log


def generateSrt(video_timecode, log):
    counter = 1
    srt_data = []
    for cur_key in video_timecode.keys():
        # print(cur_key)
        try:
            line = log[cur_key]
            # print(line)
            data_line = cur_key + '\n' + log_string_format(line) + '\n'
        except KeyError:
            data_line = cur_key + '\nNo data here'

        srt_block = str(counter) + '\n' +\
            secToTime(counter - 1) + ',000 --> ' + secToTime(counter) + ',000\n' +\
            data_line + '\n'
        srt_data.append(srt_block)
        counter += 1

    return srt_data




if __name__ == '__main__':

    path = filedialog.askdirectory(initialdir='D:/VIDEOPLATFORM_REC')
    SEC_SRT_OFFSET = 1

    v_list = getVideoList(path)
    log = readLogFile(path)

    for video in v_list:
        cur_timecode = getStartEndTime(video)
        srt_name = os.path.join(path, video.split('.')[-2] + '.srt')
        srt_data = generateSrt(cur_timecode, log)
        with open(srt_name, 'w') as srt_file:
            for line in srt_data:
                srt_file.write(line)
                srt_file.write('\n')
        print(srt_name + ' written successful')


