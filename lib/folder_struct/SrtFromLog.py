"""
This module generates srt file for video
based of known log file for Videomodule
with video name containing start and end time
"""

import os
from tkinter import filedialog




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


