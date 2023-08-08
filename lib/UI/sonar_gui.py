""" This module creates GUI that specifies file name and path, and
provides vlc recording of the file """

#import tkFileDialog, subprocess, serial, time, sonar_init, requests, threading
from tkinter import *
from tkinter import filedialog

#init_parameters = sonar_init.Get_Init_Parameters()

class Application(Frame):

    def createWidgets(self):

        #Configuration var
        labelfont = ('arial', 20)
        label_bg = 'white'
        label_fg = 'black'
        buttonfont = ('arial', 15, 'bold')

        #Buttons and text set
        self.win = Frame()
        self.win.pack(side=BOTTOM, expand=YES, fill=BOTH)
        self.buttons = Frame()
        self.buttons.pack(side=TOP, expand=YES, fill=BOTH)

        #QUIT BUTTON
        self.QUIT_button = Button(self.buttons)
        self.QUIT_button["text"] = "QUIT"
        self.QUIT_button["fg"]   = "red"
        #self.QUIT["command"] =  self.quit_it
        self.QUIT_button.config(font=buttonfont)

        # Connect button
        self.connect_button = Button(self.buttons)
        self.connect_button["text"] = "Connect"
        # self.connect_button["fg"]   = "red"
        self.connect_button.config(font=buttonfont)

        #START/STOP BUTTON
        self.start_rec_button = Button(self.buttons)
        self.start_rec_button["text"] = "Start"
        self.start_rec_button["fg"]   = "dark green"
        #self.hi_there["command"] = self.start_stop
        self.start_rec_button.config(font=buttonfont)

        #DIRECTORY CHOICE BUTTON
        self.choose_dir_button = Button(self.buttons)


        #SET DEPTH ZERO BUTTON
        self.set_depth_buton = Button(self.buttons)
        self.set_depth_buton["text"] = 'Set zero depth'
        # self.set_d["command"] = self.set_depth

        #RESET DEPTH ZERO BUTTON
        self.reset_track_button = Button(self.buttons)
        self.reset_track_button["text"] = 'Reset track'
        #self.reset_d["command"] = self.reset_depth

        #DATA LABEL
        self.data_label = Label(self.win)
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
        Frame.__init__(self, master)
        self.data_text = "INITIALIZE"
        self.pack()
        self.createWidgets()



