import time

def textShorten(input_text):
    """
    Shorts text to be short inside a button
    :param input_text:
    :return: text in 20 characters
    """
    if input_text is  None:
        return ''
    if len(input_text) > 20:
        return "%s...%s" % (input_text[:6], input_text[-12:])
    else:
       return input_text

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


def parseNMEA(nmea_string):
    """
    The function parses nmea string without heading $ sign
    """
    if nmea_string is None:
        return "NO DATA"
    try:
        nmea_string = nmea_string.split(',')
        if nmea_string[0][-3:] == "GGA":
            return tuple([nmea_string[2][:2], nmea_string[2][2:],
                                        nmea_string[3],
                                        nmea_string[4][:3], nmea_string[4][3:],
                                        nmea_string[5]])
        if nmea_string[0][-3:] == "DBT":
            return tuple([nmea_string[3], nmea_string[4]])
        if nmea_string[0][-3:] == "DBS":
            return tuple([nmea_string[3], nmea_string[4]])
        if nmea_string[0][-3:] == "MTW":
            return tuple([nmea_string[1], nmea_string[2]])
    except:
        return "NO DATA"



if __name__ == '__main__':
    for  i in range(10):
        data = 'This line number is %s \n' % i
        write_srt_string('test.srt', data, i)
        # print(string_generation(i))