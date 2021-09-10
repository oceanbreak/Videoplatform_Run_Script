import time


def string_generation(srt_timer):
    # converts number into srt time format
    return '{:0>2}'.format(srt_timer//3600) + ':' \
           + '{:0>2}'.format((srt_timer//60) % 60) + ':' \
           + '{:0>2}'.format(srt_timer % 60) + ',000'


def write_srt_string(srt_file_name, data, sec):
    # Writes one subtitle section to specified file
    with open(srt_file_name, 'a') as fs:
        fs.write(str(sec)+'\n')
        fs.write( string_generation(sec) + ' --> ' + string_generation(sec+1) + '\n')
        fs.write(data)
        fs.write("\n\n")
        print("Wring srt at sec " + str(sec))


def write_log_string(log_file_name, data):
    with open(log_file_name, 'a') as fs:
        fs.write(';'.join(data))
        fs.write('\n')


def generateFileName(prefix = 'log', extension = 'txt'):
    cur_time = time.gmtime()
    date_str = '{:0>2}'.format(cur_time.tm_mday) +  '{:0>2}'.format(cur_time.tm_mon)  + '{:0>2}'.format(cur_time.tm_year)[-2:]
    time_str = '{:0>2}'.format(cur_time.tm_hour) + '{:0>2}'.format(cur_time.tm_min)  + '{:0>2}'.format(cur_time.tm_sec)
    return prefix + '_' + date_str + '_' + time_str + '.' + extension


if __name__ == '__main__':
    for  i in range(10):
        data = 'This line number is %s \n' % i
        write_srt_string('test.srt', data, i)
        # print(string_generation(i))