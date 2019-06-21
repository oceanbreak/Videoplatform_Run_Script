""" This module creates GUI that specifies file name and path, and
provides vlc recording of the file """

import subprocess, serial, time, sonar_init, requests, threading, sonar_threading
from Tkinter import *
#import generate_buffer_navi_thread

init_parameters = sonar_init.Get_Init_Parameters()
NAVI_PORT = init_parameters['NAVI_PORT']
NAVI_RATE = init_parameters['NAVI_RATE']
NAVI_MESSAGE = init_parameters['NAVI_MESSAGE']
DEPTH_PORT = init_parameters['DEPTH_PORT']
DEPTH_RATE = init_parameters['DEPTH_RATE']
ECHO_PORT = init_parameters['ECHO_PORT']
ECHO_RATE = init_parameters['ECHO_RATE']
ECHO_MESSAGE = init_parameters['ECHO_MESSAGE']
DEPTH_MESSAGE = init_parameters['DEPTH_MESSAGE']
INCLIN_PORT = init_parameters['INCLIN_PORT']
INCLIN_RATE = init_parameters['INCLIN_RATE']

class Application(Frame):

    def start_it(self):
        print("READY WRITING SUB")
        cur_time = time.gmtime()
        date_str = '{:0>2}'.format(cur_time.tm_mday) +  '{:0>2}'.format(cur_time.tm_mon)  + '{:0>2}'.format(cur_time.tm_year)[-2:]
        time_str = '{:0>2}'.format(cur_time.tm_hour) + '{:0>2}'.format(cur_time.tm_min)  + '{:0>2}'.format(cur_time.tm_sec)
        log_file_name = date_str + '_' + time_str
        self.proc_log = subprocess.Popen('python generate_log_file.py ' + self.file_path + '/' + log_file_name , stdin=None, stdout=None, stderr=None, close_fds=True)
        self.proc_main = subprocess.Popen('python main_rec_loop.py "' + self.file_path + '"', stdin=None, stdout=None, stderr=None, close_fds=True)

    def stop_it(self):
        print "STOP WRITING SUB"
        self.proc_log.terminate()
        self.proc_main.terminate()

    def quit_it(self):
        self._navi_line.stop_writing_buffer()
        #self.proc_buffer_dep.stop()
        #self.proc_buffer_ech.terminate()
        #self.proc_buffer_com.terminate()
        self.quit()

    def change_cdtext(self, new_text):
        if len(new_text) > 15:
            self.cdtext = "..." + new_text[-15:]
        else:
            self.cdtext = new_text
        self.choose_dir["text"] = self.cdtext

    def locate(self):
        Filename = tkFileDialog.askdirectory(initialdir = 'C:/VIDEOPLATFORM_REC')
        if Filename != "":
            self.change_cdtext(Filename)
            self.file_path = Filename + '/'
            threading.Thread(target = self.change_cam_dir).start()
            print self.file_path

    def change_cam_dir(self):
        #try:
        cam_req = requests.get(self._cam_url + '/cgi-bin/capture.cgi?action=set&capture_folder=' + self.file_path, auth=self._login_pass)
        if cam_req.status_code == 200:
            print 'Camera redord in ' + self.file_path
        else:
            print 'Cannot change record folder'
        #except:
        #    print('Camera not availible')


    def start_stop(self):
        if self.rec_is_running:
            self.hi_there["text"] = "Start"
            self.hi_there["fg"]   = "dark green"
            self.stop_it()
            self.rec_is_running = False
        else:
            self.hi_there["text"] = "Stop"
            self.hi_there["fg"]   = "red"
            self.start_it()
            self.rec_is_running = True

    def set_depth(self):
        try:
            port = serial.Serial(DEPTH_PORT, DEPTH_RATE, timeout=None)   #DEPTH SENSOR set com
            port.write('set 10')
            print "===== 10m SET ====="
            port.close()
        except serial.SerialException:
            print "===== NO ACCESS TO PORT====="

    def reset_depth(self):
        try:
            port = serial.Serial(DEPTH_PORT, DEPTH_RATE, timeout=None) #DEPTH SENSOR set com
            port.write('reset')
            print "===== ZERO RESET ====="
            port.close()
        except serial.SerialException:
            print "===== NO ACCESS TO PORT ====="

    def get_text_label(self):
        try:
            input_data = str(self._navi_line.getString())
        except:
            input_data = 'Waiting for data\n'
        self.data_text = input_data + time.asctime(time.gmtime()) + " GMT"
        self.data_label["text"] = self.data_text
        #Repeat this function every second
        self.after(1000, self.get_text_label)



    def createWidgets(self):

        #Configuration var
        labelfont = ('arial', 20)
        label_bg = 'white'
        label_fg = 'black'
        buttonfont = ('arial', 15, 'bold')


        self.win = Frame()
        self.win.pack(side=BOTTOM, expand=YES, fill=BOTH)
        self.buttons = Frame()
        self.buttons.pack(side=TOP, expand=YES, fill=BOTH)

        #QUIT BUTTON
        self.QUIT = Button(self.buttons)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit_it
        self.QUIT.config(font=buttonfont)

        self.QUIT.pack({"side": "left", "expand":"YES", "fill":"both"})

        #START/STOP BUTTON
        self.hi_there = Button(self.buttons)
        self.hi_there["text"] = "Start"
        self.hi_there["fg"]   = "dark green"
        self.hi_there["command"] = self.start_stop
        self.hi_there.config(font=buttonfont)

        self.hi_there.pack({"side": "left", "expand":"YES", "fill":"both"})

        #DIRECTORY CHOICE BUTTON
        self.choose_dir = Button(self.buttons)
        self.choose_dir["text"] = self.cdtext
        self.choose_dir["command"] = self.locate

        self.choose_dir.pack({"side": "left", "expand":"YES", "fill":"both"})

        #SET DEPTH ZERO BUTTON
        self.set_d = Button(self.buttons)
        self.set_d["text"] = 'Set depth 10'
        self.set_d["command"] = self.set_depth

        self.set_d.pack({"side": "top", "expand":"YES", "fill":"both"})

        #RESET DEPTH ZERO BUTTON
        self.reset_d = Button(self.buttons)
        self.reset_d["text"] = 'Reset depth 0'
        self.reset_d["command"] = self.reset_depth

        self.reset_d.pack({"side": "bottom", "expand":"YES", "fill":"both"})

        #DATA LABEL
        self.data_label = Label(self.win)
        self.data_label["text"] = self.data_text
        self.data_label.config(font=labelfont, bg = label_bg, fg = label_fg)

        self.data_label.pack({"side": "left", "expand":"YES", "fill":"both"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.rec_is_running = False
        self.data_text = "INITIALIZE"
        self.file_path = 'C:/VIDEOPLATFORM_REC' 
        self._cam_url = 'http://192.168.0.31'
        self._login_pass = ('admin', 'admin')
        self.cdtext = self.file_path
        self._navi_line = generate_buffer_navi_thread.GenerateNavi(NAVI_PORT, NAVI_RATE, NAVI_MESSAGE)
        self._navi_line.repeat_writing_buffer()
        self.pack()
        self.createWidgets()
        self.get_text_label()
        #self.proc_buffer_dep = subprocess.Popen('python generate_buffer_depth.py' + ' ' + DEPTH_PORT + \
        #    ' ' + str(DEPTH_RATE) + ' ' + DEPTH_MESSAGE, stdin=None, stdout=None, stderr=None, close_fds=True)
        #self.proc_buffer_ech = subprocess.Popen('python generate_buffer_echo.py' + ' ' + ECHO_PORT + \
        #    ' ' + str(ECHO_RATE) + ' ' + ECHO_MESSAGE, stdin=None, stdout=None, stderr=None, close_fds=True)
        #self.proc_buffer_com = subprocess.Popen('python generate_buffer_compas.py' + ' ' + INCLIN_PORT + \
        #    ' ' + str(INCLIN_RATE), stdin=None, stdout=None, stderr=None, close_fds=True)

root = Tk()
app = Application(master=root)
app.master.title("OCEAN RECORD v3.0")
app.master.maxsize(600,300)
app.mainloop()
root.destroy()
