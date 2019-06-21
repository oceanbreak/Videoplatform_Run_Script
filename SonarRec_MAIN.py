"""
Command set for MAIN_GUI piece of program
"""

import time, sonar_init, sonar_gui, sonardatabuffer, requests
from tkinter import filedialog
from sonar_threading import SonarThread

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

    init_parameters = sonar_init.Get_Init_Parameters()
    button_change_dir_text = init_parameters['DEFAULT_FOLDER']

    def __init__(self):
        self._record_folder_path = self.init_parameters['DEFAULT_FOLDER']
        self._camera_IP = self.init_parameters['CAM_URL']
        self._login_pass =  (self.init_parameters['CAM_LOGIN'], self.init_parameters['CAM_PASSWORD'])
        self.root = sonar_gui.Tk()
        self.SonarGui = sonar_gui.Application(master=self.root)
        self.SonarGui.master.title("OCEAN RECORD v. 3.2")
        self.SonarGui.master.maxsize(600, 300)
        self.buffer_type_list = ('NAVI', 'DEPTH', 'ECHO', 'ALTIMETER')
        self.buffer_queue = [self.spanBuffer(x) for x in self.buffer_type_list]

        for buffer in self.buffer_queue:
            buffer.repeat_writing_buffer()

        self.updateDataText()
        self.setButtonsParameters()
        self.change_cam_dir()
        self.SonarGui.mainloop()


    def spanBuffer(self, data_type):
        port, rate, message = data_type + '_PORT', \
                              data_type + '_RATE', \
                              data_type + '_MESSAGE'
        return sonardatabuffer.GenerateBuffer(port, rate, message)

    def change_cam_dir(self):
        cam_req = requests.get(self._camera_IP + '/cgi-bin/capture.cgi?action=set&capture_folder=' + self._record_folder_path, auth=self._login_pass)
        if cam_req.status_code == 200:
            print('Camera record in ' + self._record_folder_path)
        else:
            print('Cannot change record folder')


    def setButtonsParameters(self):

        self.SonarGui.choose_dir_button['text'] = self.button_change_dir_text
        self.SonarGui.choose_dir_button['command'] = self.buttonChangeDirCommand

        self.SonarGui.QUIT_button['command'] = self.buttonQuitCommand

    def sendProc(self):
        return self.buffer_queue[0]

    def updateDataText(self):
        self.SonarGui.data_label['text'] = bufferCoordFormat(self.buffer_queue[0].getData()) + '\n' + \
                                           time.asctime(time.gmtime()) + " GMT"
        self.SonarGui.after(1000, self.updateDataText)

    def buttonQuitCommand(self):
        self.buffer_queue[0].stop_writing_buffer()
        self.SonarGui.quit()

    def buttonChangeDirCommand(self):
        new_file_path = filedialog.askdirectory(initialdir = self._record_folder_path)
        if new_file_path != "":
            self._record_folder_path = new_file_path
            button_change_dir_text = textShorten(new_file_path)
            self.SonarGui.choose_dir_button['text'] = button_change_dir_text
            self.change_cam_dir()


app = SonarVideoProgram()