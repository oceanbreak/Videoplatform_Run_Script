""" This module creates GUI that specifies file name and path, and
provides vlc recording of the file """

#import tkFileDialog, subprocess, serial, time, sonar_init, requests, threading
# from tkinter import *
# from tkinter import filedialog
import tkinter as Tk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo, showwarning, askyesno
import time
from PIL import Image, ImageTk

#init_parameters = sonar_init.Get_Init_Parameters()

class MainWindow(Tk.Frame):

    def popUpWarning(self, text):
        showwarning('Warning', text)

    def popError(self, text):
        showerror('Error', text)

    def popAskWindow(self, text):
        return askyesno('Confirmation', text)
    
    def setupImageOnLabel(self):
        # Add image
        self.im = Image.open('resources\image\SonarLabLogo.png').resize((200,140))
        self.ph = ImageTk.PhotoImage(self.im)

        self.data_label.config(image=self.ph)
        print('OK creating image')

    def cearImageOnLabel(self):
        self.data_label.config(image='')

    def createWidgets(self):

        #Configuration var
        labelfont = ('arial', 20)
        label_bg = 'white'
        label_fg = 'black'
        buttonfont = ('arial', 15, 'bold')

        #Buttons and text set
        self.win = Tk.Frame()
        self.win.pack(side=Tk.BOTTOM, expand=Tk.YES, fill=Tk.BOTH)
        self.buttons_field = Tk.Frame()
        self.buttons_field.pack(side=Tk.TOP, expand=Tk.NO, fill=Tk.X)

        #QUIT BUTTON
        self.QUIT_button = Tk.Button(self.buttons_field)
        self.QUIT_button["text"] = "QUIT"
        self.QUIT_button["fg"]   = "red"
        # self.QUIT_button['state'] = 'disable'
        #self.QUIT["command"] =  self.quit_it
        self.QUIT_button.config(font=buttonfont)

        # Connect button
        self.connect_button = Tk.Button(self.buttons_field)
        self.connect_button["text"] = "Connect"
        # self.connect_button['command'] = self.settingsWindow
        # self.connect_button["fg"]   = "red"
        self.connect_button.config(font=buttonfont)

        #START/STOP BUTTON
        self.start_rec_button = Tk.Button(self.buttons_field)
        self.start_rec_button["text"] = "Start"
        self.start_rec_button["fg"]   = "dark green"
        self.start_rec_button['state'] = 'disable'
        #self.hi_there["command"] = self.start_stop
        self.start_rec_button.config(font=buttonfont)

        #DIRECTORY CHOICE BUTTON
        self.cam_dialog_button = Tk.Button(self.buttons_field)
        self.cam_dialog_button['text'] = 'CAM'
        self.cam_dialog_button["fg"]   = "dark blue"
        self.cam_dialog_button['font'] = buttonfont


        #SET DEPTH ZERO BUTTON
        self.set_depth_buton = Tk.Button(self.buttons_field)
        self.set_depth_buton["text"] = 'Set zero depth'
        self.set_depth_buton['state'] = 'disable'
        # self.set_d["command"] = self.set_depth

        #RESET DEPTH ZERO BUTTON
        self.reset_track_button = Tk.Button(self.buttons_field)
        self.reset_track_button["text"] = 'Reset track'
        self.reset_track_button['state'] = 'disable'
        #self.reset_d["command"] = self.reset_depth

        # Settings
        self.settings_button = Tk.Button(self.buttons_field)
        self.settings_button['text'] = 'Settings'

        #DATA LABEL
        self.data_label = Tk.Label(self.win)
        self.data_label["text"] = self.data_text
        self.setupImageOnLabel()

        self.data_label.config(font=labelfont, bg = label_bg, fg = label_fg)

        self.settings_button.pack(side=Tk.LEFT, expand=Tk.YES, fill=Tk.BOTH)
        self.connect_button.pack({"side": "left", "expand": "YES", "fill": "both"})
        self.QUIT_button.pack({"side": "left", "expand": "YES", "fill": "both"})
        self.start_rec_button.pack({"side": "left", "expand": "YES", "fill": "both"})
        self.cam_dialog_button.pack({"side": "left", "expand": "YES", "fill": "both"})


        self.set_depth_buton.pack({"side": "top", "expand": "YES", "fill": "both"})
        self.reset_track_button.pack({"side": "bottom", "expand": "YES", "fill": "both"})

        

        # self.connect_button.grid(row=0, column=0, sticky=Tk.N)
        # self.settings_button.grid(row=1, column=0, sticky=Tk.S)
        # self.QUIT_button.grid(row=0, column=1, rowspan=2)
        # self.start_rec_button.grid(row=0, column=2, rowspan=2)
        # self.choose_dir_button.grid(row=0, column=3, rowspan=2)
        # self.set_depth_buton.grid(row=0, column=4)
        # self.reset_track_button.grid(row=1, column=4)

        

        self.data_label.pack({"side": "left", "expand":"YES", "fill":"both"})


    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.data_text = "Welcome to Sonarlab"
        self.pack()
        self.createWidgets()


    def settingsWindow(self):
        self.settings_window = SettingsWindow(self.win)
        return self.settings_window
    
    def camControlWindow(self):
        self.cam_control_window = CameraControlWindow(self.win)
        return self.cam_control_window
    

    def setButtonsActive(self):
        self.start_rec_button['state'] = 'normal'
        self.start_rec_button["fg"]   = "dark green"
        self.reset_track_button['state'] = 'normal'
        self.set_depth_buton['state'] = 'normal'


    def setButtonsInactive(self):
        self.start_rec_button['state'] = 'disable'
        # self.start_rec_button["fg"]   = "dark green"
        self.reset_track_button['state'] = 'disable'
        self.set_depth_buton['state'] = 'disable'

    def updateDataText(self, text):
        self.data_label['text'] = text



class SettingsWindow(Tk.Toplevel):

    def __init__(self, master):
        super().__init__(master=master)
        self.grab_set() # To avoid opening multiple windows
        self.createWidgets()

    def createWidgets(self):
        header_font = ('arial', 12, 'bold')

        # self.settings_window = Tk.Toplevel(self.win)
        self.geometry('520x550')
        self.title('Settings')

        # Inputs

        # Channels
        self.channels = Tk.Frame(self)
        self.channels.pack(side=Tk.TOP, expand=Tk.NO, fill=Tk.BOTH)
        self.channels_header = Tk.Label(self.channels, text = 'COM-ports settings', font = header_font)
        self.channels_header.grid(row=0, columnspan=5, pady=20, sticky=Tk.W)

        # Header
        self.chan_nm = Tk.Label(self.channels, text='Port')
        self.chan_rt = Tk.Label(self.channels, text='Rate')
        self.chan_ms = Tk.Label(self.channels, text='Message')
        self.chan_nm.grid(row=1, column=2, sticky=Tk.W)
        self.chan_rt.grid(row=1, column=3, sticky=Tk.W)
        self.chan_ms.grid(row=1, column=4, sticky=Tk.W)

        # Channel-01
        self.chan1_active = Tk.IntVar()
        self.chan1_atctivator = Tk.Checkbutton(self.channels, variable=self.chan1_active)
        self.chan1_name = Tk.Label(self.channels, text='Navigation')
        self.chan1_port = Tk.Entry(self.channels)
        self.chan1_rate = Tk.Entry(self.channels)
        self.chan1_message = Tk.Entry(self.channels)

        self.chan1_atctivator.grid(row=2, column=0)
        self.chan1_name.grid(row=2, column=1, sticky=Tk.W)
        self.chan1_port.grid(row=2, column=2)
        self.chan1_rate.grid(row=2, column=3)
        self.chan1_message.grid(row=2, column=4)

        # Channel-02
        self.chan2_active = Tk.IntVar()
        self.chan2_atctivator = Tk.Checkbutton(self.channels, variable=self.chan2_active)
        self.chan2_name = Tk.Label(self.channels, text='Depth')
        self.chan2_port = Tk.Entry(self.channels)
        self.chan2_rate = Tk.Entry(self.channels)
        self.chan2_message = Tk.Entry(self.channels)
        
        self.chan2_atctivator.grid(row=3, column=0)
        self.chan2_name.grid(row=3, column=1, sticky=Tk.W)
        self.chan2_port.grid(row=3, column=2)
        self.chan2_rate.grid(row=3, column=3)
        self.chan2_message.grid(row=3, column=4)

        # Channel-03
        self.chan3_active = Tk.IntVar()
        self.chan3_atctivator = Tk.Checkbutton(self.channels, variable=self.chan3_active)
        self.chan3_name = Tk.Label(self.channels, text='Altimeter')
        self.chan3_port = Tk.Entry(self.channels)
        self.chan3_rate = Tk.Entry(self.channels)
        self.chan3_message = Tk.Entry(self.channels)

        self.chan3_atctivator.grid(row=4, column=0)
        self.chan3_name.grid(row=4, column=1, sticky=Tk.W)
        self.chan3_port.grid(row=4, column=2)
        self.chan3_rate.grid(row=4, column=3)
        self.chan3_message.grid(row=4, column=4)

        # Channel-04
        self.chan4_active = Tk.IntVar()
        self.chan4_atctivator = Tk.Checkbutton(self.channels, variable=self.chan4_active)
        self.chan4_name = Tk.Label(self.channels, text='Temperature')
        self.chan4_port = Tk.Entry(self.channels)
        self.chan4_rate = Tk.Entry(self.channels)
        self.chan4_message = Tk.Entry(self.channels)

        self.chan4_atctivator.grid(row=5, column=0)
        self.chan4_name.grid(row=5, column=1, sticky=Tk.W)
        self.chan4_port.grid(row=5, column=2)
        self.chan4_rate.grid(row=5, column=3)
        self.chan4_message.grid(row=5, column=4)

        # Channel-06
        self.chan6_active = Tk.IntVar()
        self.chan6_atctivator = Tk.Checkbutton(self.channels, variable=self.chan6_active)
        self.chan6_name = Tk.Label(self.channels, text='Ship Sonar')
        self.chan6_port = Tk.Entry(self.channels)
        self.chan6_rate = Tk.Entry(self.channels)
        self.chan6_message = Tk.Entry(self.channels)

        self.chan6_atctivator.grid(row=6, column=0)
        self.chan6_name.grid(row=6, column=1, sticky=Tk.W)
        self.chan6_port.grid(row=6, column=2)
        self.chan6_rate.grid(row=6, column=3)
        self.chan6_message.grid(row=6, column=4)

        # Channel-05
        self.chan5_active = Tk.IntVar()
        self.chan5_atctivator = Tk.Checkbutton(self.channels, variable=self.chan5_active)
        self.chan5_name = Tk.Label(self.channels, text='Inclinometer')
        self.chan5_port = Tk.Entry(self.channels)
        self.chan5_rate = Tk.Entry(self.channels)
        # self.chan5_message = Tk.Entry(self.channels)

        self.chan5_atctivator.grid(row=7, column=0)
        self.chan5_name.grid(row=7, column=1, sticky=Tk.W)
        self.chan5_port.grid(row=7, column=2)
        self.chan5_rate.grid(row=7, column=3)
        # self.chan5_message.grid(row=6, column=4)


        # Camera Settings
        self.cam_settings = Tk.Frame(self)
        self.cam_settings.pack(side=Tk.TOP, expand=Tk.NO, fill=Tk.BOTH)
        self.cam_header = Tk.Label(self.cam_settings, text = 'IP-camera settings', font = header_font)
        self.cam_header.grid(row=0, columnspan=2, pady=20, sticky=Tk.W)

        self.cam_IP_label = Tk.Label(self.cam_settings, text='URL')
        self.cam_IP_entry = Tk.Entry(self.cam_settings)
        self.cam_IP_label.grid(row=1, column=0, sticky=Tk.W)
        self.cam_IP_entry.grid(row=1, column=1)

        self.cam_login_label = Tk.Label(self.cam_settings, text='Login')
        self.cam_login_entry = Tk.Entry(self.cam_settings)
        self.cam_login_label.grid(row=2, column=0, sticky=Tk.W)
        self.cam_login_entry.grid(row=2, column=1)

        self.cam_password_label = Tk.Label(self.cam_settings, text='Password')
        self.cam_password_entry = Tk.Entry(self.cam_settings)
        self.cam_password_label.grid(row=3, column=0, sticky=Tk.W)
        self.cam_password_entry.grid(row=3, column=1)

        self.default_folder_label = Tk.Label(self.cam_settings, text='Recording folder', font = header_font)
        self.default_folder_label.grid(row=4, column=0, columnspan=2, pady=10)
        self.default_folder_button = Tk.Button(self.cam_settings)
        self.default_folder_button.grid(row=5, columnspan=2, sticky=Tk.W, pady=10)

        self.log_file_freq_label = Tk.Label(self.cam_settings, text='Log frequency (sec)')
        self.log_file_freq_entry = Tk.Entry(self.cam_settings)
        self.log_file_freq_label.grid(row=6, column=0, sticky=Tk.W)
        self.log_file_freq_entry.grid(row=6, column=1)

        self.UTC_time_label = Tk.Label(self.cam_settings, text='Time in UTC')
        self.UTC_active = Tk.IntVar()
        self.UTC_activator = Tk.Checkbutton(self.cam_settings, variable=self.UTC_active)
        self.UTC_time_label.grid(row=7, column=0, sticky=Tk.W)
        self.UTC_activator.grid(row=7, column=1, sticky=Tk.W)


        # Bottom buttons
        self.bottom_buttons = Tk.Frame(self)
        self.bottom_buttons.pack(side=Tk.TOP, expand=Tk.YES, fill=Tk.BOTH, pady=10, padx=10)

        self.close_button = Tk.Button(self.bottom_buttons)
        self.close_button['text'] = 'Close'
        self.close_button['command'] = self.destroy
        self.close_button.pack(side=Tk.RIGHT, pady=5, padx=5)

        self.apply_button = Tk.Button(self.bottom_buttons)
        self.apply_button['text'] = 'Apply'
        self.apply_button.pack(side=Tk.RIGHT, pady=5, padx=5)


class CameraControlWindow(Tk.Toplevel):
    
    def __init__(self, master):
        super().__init__(master=master)
        self.grab_set()
        self.createWidgets()


    def createWidgets(self):

        self.geometry('200x300')
        self.title('Camera Control Panel')
        
        self.connect_button = Tk.Button(self)
        self.connect_button['text'] = 'Connect camera'

        self.sync_time_button = Tk.Button(self)
        self.sync_time_button['text'] = 'Sync time'
        self.sync_time_button.config(state=Tk.DISABLED)

        self.rec_sd_button = Tk.Button(self)
        self.rec_sd_button['text'] = 'Start SD Recording'
        self.rec_sd_button.config(state=Tk.DISABLED)

        self.format_sd_button = Tk.Button(self)
        self.format_sd_button['text'] = 'Format SD'
        self.format_sd_button.config(state=Tk.DISABLED)

        self.download_button = Tk.Button(self)
        self.download_button['text'] = 'Download'
        self.download_button.config(state=Tk.DISABLED)

        self.download_progress = ttk.Progressbar(self, orient=Tk.HORIZONTAL, length=200)

        self.close_button = Tk.Button(self)
        self.close_button['text'] = 'Close'
        self.close_button['command'] = self.destroy

        self.connect_button.pack(side=Tk.TOP, fill=Tk.BOTH, expand=Tk.YES)
        self.sync_time_button.pack(side=Tk.TOP, fill=Tk.BOTH, expand=Tk.YES)
        self.rec_sd_button.pack(side=Tk.TOP, fill=Tk.BOTH, expand=Tk.YES)
        self.format_sd_button.pack(side=Tk.TOP, fill=Tk.BOTH, expand=Tk.YES)
        self.download_button.pack(side=Tk.TOP, fill=Tk.BOTH, expand=Tk.YES)
        self.download_progress.pack(side=Tk.TOP, fill=Tk.BOTH, expand=Tk.YES)
        self.close_button.pack(side=Tk.TOP, fill=Tk.BOTH, expand=Tk.YES)


    def deactivateButtons(self):
        self.sync_time_button.config(state=Tk.DISABLED)
        self.rec_sd_button.config(state=Tk.DISABLED)
        self.format_sd_button.config(state=Tk.DISABLED)
        self.download_button.config(state=Tk.DISABLED)


    def activateButtons(self):
        self.sync_time_button.config(state=Tk.NORMAL)
        self.rec_sd_button.config(state=Tk.NORMAL)
        self.format_sd_button.config(state=Tk.NORMAL)
        self.download_button.config(state=Tk.NORMAL)





if  __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
