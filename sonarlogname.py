""" This module genertes name for file based on current date and time with prefix ('log' by default)"""
import time

def generateFileName(prefix = 'log'):
    cur_time = time.gmtime()
    date_str = '{:0>2}'.format(cur_time.tm_mday) +  '{:0>2}'.format(cur_time.tm_mon)  + '{:0>2}'.format(cur_time.tm_year)[-2:]
    time_str = '{:0>2}'.format(cur_time.tm_hour) + '{:0>2}'.format(cur_time.tm_min)  + '{:0>2}'.format(cur_time.tm_sec)
    return prefix + '_' + date_str + '_' + time_str

if __name__ == '__main__':
     for i in range(10):
         print(generateFileName())
         time.sleep(2)