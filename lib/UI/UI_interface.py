""" This module creates GUI that specifies file name and path, and
provides vlc recording of the file """

#import tkFileDialog, subprocess, serial, time, sonar_init, requests, threading
# from tkinter import *
# from tkinter import filedialog
import tkinter as Tk

#init_parameters = sonar_init.Get_Init_Parameters()

class Application(Tk.Frame):

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
        self.buttons_field.pack(side=Tk.TOP, expand=Tk.YES, fill=Tk.BOTH)

        #QUIT BUTTON
        self.QUIT_button = Tk.Button(self.buttons_field)
        self.QUIT_button["text"] = "QUIT"
        self.QUIT_button["fg"]   = "red"
        #self.QUIT["command"] =  self.quit_it
        self.QUIT_button.config(font=buttonfont)

        # Connect button
        self.connect_button = Tk.Button(self.buttons_field)
        self.connect_button["text"] = "Connect"
        self.connect_button['command'] = self.settingsWindow
        # self.connect_button["fg"]   = "red"
        self.connect_button.config(font=buttonfont)

        #START/STOP BUTTON
        self.start_rec_button = Tk.Button(self.buttons_field)
        self.start_rec_button["text"] = "Start"
        self.start_rec_button["fg"]   = "dark green"
        #self.hi_there["command"] = self.start_stop
        self.start_rec_button.config(font=buttonfont)

        #DIRECTORY CHOICE BUTTON
        self.choose_dir_button = Tk.Button(self.buttons_field)


        #SET DEPTH ZERO BUTTON
        self.set_depth_buton = Tk.Button(self.buttons_field)
        self.set_depth_buton["text"] = 'Set zero depth'
        # self.set_d["command"] = self.set_depth

        #RESET DEPTH ZERO BUTTON
        self.reset_track_button = Tk.Button(self.buttons_field)
        self.reset_track_button["text"] = 'Reset track'
        #self.reset_d["command"] = self.reset_depth

        #DATA LABEL
        self.data_label = Tk.Label(self.win)
        self.data_label["text"] = self.data_text
        self.data_label.config(font=labelfont, bg = label_bg, fg = label_fg)

        self.connect_button.pack({"side": "left", "expand": "YES", "fill": "both"})
        self.QUIT_button.pack({"side": "left", "expand": "YES", "fill": "both"})
        self.start_rec_button.pack({"side": "left", "expand": "YES", "fill": "both"})
        self.choose_dir_button.pack({"side": "left", "expand": "YES", "fill": "both"})
        self.set_depth_buton.pack({"side": "top", "expand": "YES", "fill": "both"})
        self.reset_track_button.pack({"side": "bottom", "expand": "YES", "fill": "both"})
        self.data_label.pack({"side": "left", "expand":"YES", "fill":"both"})


    def __init__(self, master=None):
        Tk.Frame.__init__(self, master)
        self.data_text = "INITIALIZE"
        self.pack()
        self.createWidgets()



    def settingsWindow(self):

        self.settings_window = SettingsWindow(self.win)



class SettingsWindow(Tk.Toplevel):

    def __init__(self, master):
        super().__init__(master=master)
        self.createWidgets()

    def createWidgets(self):
        header_font = ('arial', 12, 'bold')

        # self.settings_window = Tk.Toplevel(self.win)
        self.geometry('600x260')
        self.title('Settings')

        # Inputs

        # Channel 1
        self.channels = Tk.Frame(self)
        self.channels.pack(side=Tk.TOP, expand=Tk.YES, fill=Tk.BOTH)
        self.channels_header = Tk.Label(self.channels, text = 'COM-ports settings', font = header_font)
        self.channels_header.grid(row=0, columnspan=5, pady=20)

        # Header
        self.chan_nm = Tk.Label(self.channels, text='Port')
        self.chan_rt = Tk.Label(self.channels, text='Rate')
        self.chan_ms = Tk.Label(self.channels, text='Message')
        self.chan_nm.grid(row=1, column=2, sticky=Tk.W)
        self.chan_rt.grid(row=1, column=3, sticky=Tk.W)
        self.chan_ms.grid(row=1, column=4, sticky=Tk.W)

        # Channel-01
        self.chan1_atctivator = Tk.Checkbutton(self.channels)
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
        self.chan2_atctivator = Tk.Checkbutton(self.channels)
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
        self.chan3_atctivator = Tk.Checkbutton(self.channels)
        self.chan3_name = Tk.Label(self.channels, text='Altimeter')
        self.chan3_port = Tk.Entry(self.channels)
        self.chan3_rate = Tk.Entry(self.channels)
        self.chan3_message = Tk.Entry(self.channels)

        self.chan3_atctivator.grid(row=4, column=0)
        self.chan3_name.grid(row=4, column=1, sticky=Tk.W)
        self.chan3_port.grid(row=4, column=2)
        self.chan3_rate.grid(row=4, column=3)
        self.chan3_message.grid(row=4, column=4)




if  __name__ == '__main__':
    app = Application()
    app.mainloop()
