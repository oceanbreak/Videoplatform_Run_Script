import time
import os
from lib.data.DataCollection import DataCollection

class SrtGenerator:

    def __init__(self, video_file : str, data_collection : DataCollection):
        self.video_file = video_file
        self.data_collection = data_collection

    def string_generation(self, srt_timer):
        # converts number into srt time format
        return '{:0>2}'.format(srt_timer//3600) + ':' \
            + '{:0>2}'.format((srt_timer//60) % 60) + ':' \
            + '{:0>2}'.format(srt_timer % 60) + ',000'


    def write_srt_string(self, data, sec):
        # Writes one subtitle section to specified file
        with open(self.srt_file_name, 'a') as fs:
            fs.write(str(sec)+'\n')
            fs.write( self.string_generation(sec) + ' --> ' + self.string_generation(sec+1) + '\n')
            fs.write(data)
            fs.write("\n\n")
            print("Wring srt at sec " + str(sec))


    def generateSrtFile(self):
        self.srt_file_name = '.'.join(self.video_file.split('.')[:-1]) + '.srt'
        cur_size = os.path.getsize(self.video_file)
        time.sleep(0.5)

        cur_sec = 1

        while True:
            new_size = os.path.getsize(self.video_file)
            if new_size <= cur_size:
                print('   STOP SRT generation for ' + self.video_file)
                break
            cur_size = new_size

            self.write_srt_string(self.dataCollection.toDisplayText(), cur_sec)
            cur_sec += 1
            time.sleep(1)