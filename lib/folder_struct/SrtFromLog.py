"""
This module generates srt file for video
based of known log file for Videomodule
with video name containing start and end time
"""

#TODO SRT delay 2 seconds

import os
from tkinter import filedialog
from lib.UI.Settings import Settings
from lib.data.DataCollection import DataCollection
from lib.data.DataStructure import *
from lib.folder_struct.SrtGenerator import SrtGenerator
from lib.data.DataStructure import DateTime
from datetime import datetime, timedelta


class SrtFromLog:

    video_format_list = ['avi', 'AVI', 'mp4', 'MP4']

    def __init__(self, settings : Settings, data_collection : DataCollection):
        self.data_collection = data_collection
        self.settings = settings
        self.folder_path = None
        self.log_data = None

    def askFolder(self):
        ret = filedialog.askdirectory(initialdir=self.settings.default_folder)
        if ret != '':
            self.folder_path = ret
        return ret

    def getVideoList(self):
        self.video_list = [name for name in os.listdir(self.folder_path) 
                           if name.split('.')[-1] in self.video_format_list
                            and name[0]=='R']
        
    def getLogList(self):
        self.log_list = [name for name in os.listdir(self.folder_path) if name.split('.')[-1] == 'csv']


    def readLogData(self):
        log_reader = LogReader('', self.data_collection)
        for log_file in self.log_list:
            path = os.path.join(self.folder_path, log_file)
            log_reader.readLogFile(path)
        self.log_data = log_reader.getLogData()
        return self.log_data
    

    def writeSrt(self, video_file_name):
        srt_data = [] # Initialize SRT data
        video_full = os.path.join(self.folder_path, video_file_name)
        srt_gen = SrtGenerator(video_full, self.data_collection)
        
        video_timer = VideoTimer(video_file_name)
        video_timer.parseVideoName()
        duration = video_timer.videoTimeToSeconds()

        for cur_sec in range(duration):
            cur_timestamp = video_timer.getCurSecond()
            # print(cur_timestamp.toLogTimestamp())
            try:
                srt_data.append(self.log_data[cur_timestamp.toLogTimestamp()].toSrtString())
            except KeyError:
                srt_data.append('No data')
            video_timer.incrementVideoSecond()
        
        srt_gen.write_srt_data(srt_data)


    def iterateOverVideos(self):
        for video_file in self.video_list:
            print(f'Generating Subtitles for {video_file}')
            self.writeSrt(video_file)          

    
    def run(self):
        ret = self.askFolder()
        if ret == '':
            print('No folder specified')
            return 0
        try:
            self.getVideoList()
            self.getLogList()
            print(f'Found {len(self.video_list)} videos in folder: ', self.video_list)
            print(f'Found {len(self.log_list)} log_files in folder: ', self.log_list)
            self.readLogData()
            self.iterateOverVideos()
            return 1
        except ValueError as e:
            print('Error occured', e)
            return 0

        

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
        
class LogData(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def timestamps(self):
        return self.keys()
    
    def loglines(self):
        return self.values()


class LogReader:
    
    # Class that stores data read from log-file
    # based on its header

    def __init__(self, log_file_path, data_collection : DataCollection):
        self.data_collection = data_collection
        self.log_file_path = log_file_path
        
        self.map_header = data_collection.logHeader(ignore_enabled=True)
        self.header = None
        # print(self.full_header)

        self.log_data = LogData()

    def readLogHeader(self):
        # Read header
        # :return list of data types with column numbers

        with open(self.log_file_path, 'r') as log:
            header_string = log.readline().rstrip().split(';')

        return header_string
    
    def readLogFile(self, log_file_path=''):
        # Form log_data that is dictionary with keys - time stamps,
        # values - LogString objects

        # Update file path if needed
        if log_file_path != '':
            self.log_file_path = log_file_path
        i=0
        with open(self.log_file_path, 'r') as log:
            for line in log:
                if i==0:
                    self.header = self.readLogHeader()
                else:
                    line = line.rstrip().split(';')
                    log_line = LogString(self.header, line, self.map_header)
                    timestamp = (log_line.date.value, log_line.time.value)
                    # timestamp.logStamp(log_line.date.value, log_line.time.value)
                    self.log_data[timestamp] = log_line
                i+=1

    def getLogData(self):
        return self.log_data



class VideoTimer:

    def __init__(self, video_file):
        self.video_file = '.'.join(video_file.split('.')[:-1])


    def parseVideoName(self):
        try:
            pref, start_date, start_time, end_date, end_time = self.video_file.split('_')
            self.time_start = TimeStamp().videoBewardStamp(start_date, start_time)
            self.time_end = TimeStamp().videoBewardStamp(end_date, end_time)
        except ValueError:
            print('Invalid video name')


    def videoTimeToSeconds(self):
        self.video_length = TimeStamp.differenceInSec(self.time_start, self.time_end)
        return self.video_length
    
    def incrementVideoSecond(self):
        # Increment start to 1 second
        return self.time_start.addSeconds()
    
    def getCurSecond(self):
        return self.time_start
    


class TimeStamp:
    # Class for SrtFromLog

    def __init__(self):
        self.year = None
        self.month = None
        self.day = None
        self.hour = None
        self.minute = None
        self.second = None

    def logStamp(self, date, time):
        # Makes data from log time_samp of format
        # YYYY/MM/DD, hh":mm:ss
        self.year, self.month, self.day = map(int, date.split('/'))
        self.hour, self.minute, self.second = map(int, time.split(':'))
        return self

    def videoBewardStamp(self, date, time):
        self.year = int(date[0:4])
        self.month = int(date[4:6])
        self.day = int(date[6:8])
        self.hour = int(time[0:2])
        self.minute = int(time[2:4])
        self.second = int(time[4:6])
        return self
        

    def __str__(self):
        return f'{self.year}/{self.month}/{self.day} {self.hour}:{self.minute}:{self.second}'
    
    def __eq__(self, other):
        return self.year == other.year and self.month == other.month and \
                self.day == other.day and self.hour == other.hour and \
                self.minute == other.minute and self.second == other.second
    
    def addSeconds(self, secs=1):
        # Add amount of seconds to current time
        t1 = datetime(self.year, self.month, self.day, self.hour, self.minute, self.second)
        t2 = t1 + timedelta(seconds=secs)
        self.year = t2.year
        self.month = t2.month
        self.day = t2.day
        self.hour  = t2.hour
        self.minute = t2.minute
        self.second = t2.second
        return self
        
    
    def toSeconds(self):
        # Return stored time in seconds where 0 - begin of the day
        # Year, month and day ignored
        return self.second + self.minute * 60 + self.hour * 3600
    

    def toLogTimestamp(self):
        return f'{self.year}/{self.month:0>2}/{self.day:0>2}', \
                f'{self.hour:0>2}:{self.minute:0>2}:{self.second:0>2}'

    
    @staticmethod
    def differenceInSec(time_begin , time_end):
        # Check if it's next day
        if time_end.year > time_begin.year or \
            time_end.month > time_begin.month or \
            time_end.day > time_begin.day:
            addition = 3600 * 24
        else:
            addition = 0
        # Calculate difference of wto  time stamps
        return addition + time_end.toSeconds() - time_begin.toSeconds()
    


