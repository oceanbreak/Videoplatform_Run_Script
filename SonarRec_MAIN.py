"""
Command set for MAIN_GUI piece of program
update 4.3:
    - added snaphot_log file for photos
    - added reset zero depth function
"""

import time
import os
import lib.UI.Settings as Settings
import lib.UI.UI_interface as UI_interface
from lib.data.BufferGenerator import BufferGenerator
import requests
import lib.folder_struct.sonar_img_caption as sonar_img_caption
from threading import Thread
from tkinter import filedialog
from lib.folder_struct.Utils import *
from lib.calculations.CoordinateCalc import *


#Global values
degree_sign= u'\N{DEGREE SIGN}'


#Helper functions
def textShorten(input_text):
    """
    Shorts text to be short inside a button
    :param input_text:
    :return: text in 20 characters
    """
    if len(input_text) > 20:
        return "%s...%s" % (input_text[:6], input_text[-12:])
    else:
       return input_text


def bufferCoordFormat(input_list):
    try:
        return input_list[0] + ": " +\
               degree_sign.join(input_list[1:3]) + input_list[3] + '  ' +\
               degree_sign.join(input_list[4:6]) + input_list[6]
    except TypeError:
        return str(input_list)


class SonarVideoProgram:

    init_parameters = Settings.getInitParameters()
    button_change_dir_text = init_parameters['DEFAULT_FOLDER']


    def __init__(self):
        self._is_running = False
        self._record_folder_path = self.init_parameters['DEFAULT_FOLDER']
        self._camera_IP = self.init_parameters['CAM_URL']
        self._login_pass =  (self.init_parameters['CAM_LOGIN'], self.init_parameters['CAM_PASSWORD'])
        self.root = UI_interface.Tk()
        self.SonarGui = UI_interface.Application(master=self.root)
        self.SonarGui.master.title("OCEAN RECORD v. 4.3.1")
        self.SonarGui.master.maxsize(600, 300)

        # self.buffer_type_list = ('NAVI', 'DEPTH', 'ALTIMETER' )
        self.buffer_type_list = ['NAVI']
        self.buffer_queue = [self.spanBuffer(x) for x in self.buffer_type_list]
        for buffer in self.buffer_queue:
            buffer.repeat_writing_buffer()


        # Data types
        self.navigation_data = None
        self.depth_data = None
        self.altimeter_data = None
        self.temperature_data = None
        self.gyro_data = None

        # Data dependencies
        self.data_sources = {'NAVI' : None, 'DEPTH' : None, 'ALTIMETER' : None, 'TEMP' : None, 'GYRO' : None}

        self.scan_dir = None
        self.logging = None
        self._track_length = 0.0
        self._snaps_count = 0

        self.updateDataText()
        self.setButtonsParameters()
        # self.change_cam_dir()
        self.SonarGui.mainloop()


    def spanBuffer(self, data_type):
        port, rate, message = data_type + '_PORT', \
                              data_type + '_RATE', \
                              data_type + '_MESSAGE'
        return BufferGenerator(self.init_parameters[port],
                                              self.init_parameters[rate],
                                              self.init_parameters[message])


    def change_cam_dir(self):
        cam_req = requests.get(self._camera_IP + '/cgi-bin/capture.cgi?action=set&capture_folder='
                               + self._record_folder_path, auth=self._login_pass)
        if cam_req.status_code == 200:
            print('Camera record in ' + self._record_folder_path)
        else:
            print('Cannot change record folder')


    def scanDir(self):
        # Initialize list
        file_path = self._record_folder_path + '/'
        print("=== Subtitle initialized ===")
        init_file_list = os.popen('dir "' + file_path + '" /B').readlines()
        current_file_list = init_file_list
        begin_coord = self.buffer_queue[0].getData()
        begin_coord = convertCoordtoDeg(*begin_coord)

        # Loop that checks for new avi files and starts subtitle generation
        while self._is_running:
            end_coord = self.buffer_queue[0].getData()
            end_coord = convertCoordtoDeg(*end_coord)
            self._track_length += calculateTrack(begin_coord, end_coord)
            begin_coord = end_coord
            temp_file_list = os.popen('dir "' + file_path + '" /B').readlines()
            if len(temp_file_list) > len(current_file_list):
                new_item = [item for item in temp_file_list if item not in current_file_list][0]

                # Check for video
                if new_item[-4:-1] == 'avi':
                    cur_file_name = new_item[:-1]
                    print('New video ' + file_path +  cur_file_name + ' added')
                    srt = Thread(target=self.generateSrtFile, args=[file_path +  cur_file_name])
                    srt.start()

                # Check for snapshots
                if new_item[-4:-1] == 'jpg' or new_item[-4:-1] == 'JPG':
                    cur_img_name = new_item[:-1]
                    print('New image %s added' % (file_path +  cur_img_name))
                    time.sleep(0.1)
                    snapshot_text = self.SonarGui.data_label['text']
                    sonar_img_caption.addCaption(file_path +  cur_img_name, snapshot_text)
                    with open(self._record_folder_path + '/SNAP_LOG.txt', 'a') as snapshot_log:
                        snapshot_log.write('SNAP %s: ' % '{:0>3}'.format(self._snaps_count))
                        snapshot_log.write(new_item.rstrip().split('/')[-1] + '\n')
                        snapshot_log.write(snapshot_text + '\n\n')
                        self._snaps_count += 1

                current_file_list = temp_file_list
            elif len(temp_file_list) < len(current_file_list):
                current_file_list = temp_file_list


    def generateSrtFile(self, video_file_name):
        srt_file_name = '.'.join(video_file_name.split('.')[:-1]) + '.srt'
        cur_size = os.path.getsize(video_file_name)
        time.sleep(0.5)
        # cur_sec = 1
        cur_sec = self.init_parameters['SRT_OFFSET']
        cur_sec = int(cur_sec)
        # real_sec = datetime.now().second
        while True:
            new_size = os.path.getsize(video_file_name)
            if new_size <= cur_size:
                print('   STOP SRT generation for ' + video_file_name)
                break
            cur_size = new_size
            # if datetime.now().second > real_sec or \
            #     datetime.now().second == 0 and real_sec == 59:
            #     real_sec = datetime.now().second
            write_srt_string(srt_file_name,  self.SonarGui.data_label['text'], cur_sec)
            cur_sec += 1
            time.sleep(1)


    def generateLogFile(self, log_file_name):
        while self._is_running:
            cur_time = time.gmtime()
            date_str = '/'.join(['{:0>2}'.format(cur_time.tm_mday), '{:0>2}'.format(cur_time.tm_mon),  '{:0>2}'.format(
                cur_time.tm_year)])
            time_str =  ':'.join(['{:0>2}'.format(cur_time.tm_hour), '{:0>2}'.format(cur_time.tm_min), '{:0>2}'.format(
                cur_time.tm_sec)])

            data_list = ['{0:.1f}'.format(self._track_length)] + \
                        [y for x in self.buffer_queue if x.getData() for y in x.getData() ] + \
                        [date_str, time_str]

            write_log_string(log_file_name, data_list)
            time.sleep(1.0)


    def setButtonsParameters(self):

        self.SonarGui.choose_dir_button['text'] = self.button_change_dir_text
        self.SonarGui.choose_dir_button['command'] = self.buttonChangeDirCommand

        self.SonarGui.QUIT_button['command'] = self.buttonQuitCommand

        self.SonarGui.start_rec_button['command'] = self.buttonStartCommand

        self.SonarGui.set_depth_buton['command'] = self.buttonSetDepthCommand
        self.SonarGui.reset_track_button['command'] = self.buttonResetTrackCommand


    def updateDataText(self):
        string_print = ''
        for data_name, data_value in zip(self.buffer_type_list, self.buffer_queue):
            if data_value.getData():
                string_print += data_name[:3] + ': ' + ' '.join(data_value.getData()) + '\n'
        string_print += 'Distance: ' + '{0:.1f}'.format(self._track_length) + ' m\n'
        string_print += time.asctime(time.gmtime()) + " GMT"

        # self.SonarGui.data_label['text'] = '\n'.join([' '.join(x.getData())
        #                                     for x in self.buffer_queue if x.getData()]) +  \
        #                                    '\n' + time.asctime(time.gmtime()) + " GMT"
        self.SonarGui.data_label['text'] = string_print
        self.SonarGui.after(100, self.updateDataText)


    def buttonStartCommand(self):
        if not self._is_running:
            self._is_running = True
            log_file_name = self._record_folder_path + '/' + generateFileName('videomodule_log', 'csv')
            self.logging = Thread(target=self.generateLogFile, args=[log_file_name])
            self.logging.start()
            self.scan_dir = Thread(target=self.scanDir, args=[])
            self.scan_dir.start()
            self.SonarGui.start_rec_button['text'] = 'Stop'
            self.SonarGui.start_rec_button['fg'] = 'red'
        else:
            self.SonarGui.start_rec_button['text'] = 'Start'
            self.SonarGui.start_rec_button['fg'] = 'dark green'
            self._is_running = False
            self.scan_dir.join()
            self.logging.join()


    def buttonQuitCommand(self):
        for buffer in self.buffer_queue:
           buffer.stop_writing_buffer()
        self.SonarGui.quit()


    def buttonChangeDirCommand(self):
        new_file_path = filedialog.askdirectory(initialdir = self._record_folder_path)
        if new_file_path != "":
            self._record_folder_path = new_file_path
            button_change_dir_text = textShorten(new_file_path)
            self.SonarGui.choose_dir_button['text'] = button_change_dir_text
            self.change_cam_dir()


    def buttonSetDepthCommand(self):
        # p = sonarcom.ComPortData(self.init_parameters['DEPTH_PORT'],
        #                          self.init_parameters['DEPTH_RATE'],
        #                          10,
        #                          self.init_parameters['DEPTH_MESSAGE'])
        # p.sendMessage(b'set 10')
        # p.closePort()
        self.buffer_queue[1].send_message(b'set 0')


    def buttonResetTrackCommand(self):
        self._track_length = 0.0
        self._snaps_count = 0


if __name__ == '__main__':
    app = SonarVideoProgram()