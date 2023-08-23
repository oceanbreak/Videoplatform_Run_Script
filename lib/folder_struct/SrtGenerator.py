import time
import os
from lib.data.DataCollection import DataCollection
from lib.data.SonarThread import SonarThread


# TODO Test if it continues runnong after video file stops growing
class SrtGenerator:

    def __init__(self, video_file : str, data_collection : DataCollection):
        self.video_file = video_file
        self.data_collection = data_collection
        self.srt_file_name = '.'.join(self.video_file.split('.')[:-1]) + '.srt'
        self.stop_flag = False
        self.cur_size = os.path.getsize(self.video_file)
        self.cur_sec = 0
        time.sleep(2.0)



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
            # print(f"Wring srt {self.srt_file_name} at sec " + str(sec))

    def write_srt_data(self, data):
        with open(self.srt_file_name, 'w') as fs:
            for sec in range(len(data)):
                fs.write(str(sec)+'\n')
                fs.write( self.string_generation(sec) + ' --> ' + self.string_generation(sec+1) + '\n')
                fs.write(data[sec])
                fs.write("\n\n")



    def generateSrtFile(self):
        # print('I am still here')
        while True:
            new_size = os.path.getsize(self.video_file)
            if new_size <= self.cur_size:
                print('   STOP SRT generation for ' + self.video_file)
                break
            self.cur_size = new_size

            self.write_srt_string(self.data_collection.toDisplayText(), self.cur_sec)
            self.cur_sec += 1
            time.sleep(1)