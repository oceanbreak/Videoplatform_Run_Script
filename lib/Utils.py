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


def write_log_string(log_file_name, data):
    with open(log_file_name, 'a') as fs:
        fs.write(';'.join(data))
        fs.write('\n')


def generateFileName(prefix = 'log', extension = 'txt'):
    cur_time = time.gmtime()
    date_str = '{:0>2}'.format(cur_time.tm_mday) +  '{:0>2}'.format(cur_time.tm_mon)  + '{:0>2}'.format(cur_time.tm_year)[-2:]
    time_str = '{:0>2}'.format(cur_time.tm_hour) + '{:0>2}'.format(cur_time.tm_min)  + '{:0>2}'.format(cur_time.tm_sec)
    return prefix + '_' + date_str + '_' + time_str + '.' + extension
