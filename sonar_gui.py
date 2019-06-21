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

        #START/STOP BUTTON
        self.start_rec_button = Button(self.buttons)
        self.start_rec_button["text"] = "Start"
        self.start_rec_button["fg"]   = "dark green"
        #self.hi_there["command"] = self.start_stop
        self.start_rec_button.config(font=buttonfont)

        #DIRECTORY CHOICE BUTTON
        self.choose_dir_button = Button(self.buttons)
        #self.choose_dir["text"] = self.MasterProgram.button_change_dir_text
        #self.choose_dir["command"] = self.MasterProgram.buttonChangeDirCommand(self.choose_dir)

        #SET DEPTH ZERO BUTTON
        self.set_depth_buton = Button(self.buttons)
        self.set_depth_buton["text"] = 'Set depth 10'
        #self.set_d["command"] = self.set_depth

        #RESET DEPTH ZERO BUTTON
        self.reset_depth_button = Button(self.buttons)
        self.reset_depth_button["text"] = 'Reset depth 0'
        #self.reset_d["command"] = self.reset_depth

        #DATA LABEL
        self.data_label = Label(self.win)
        self.data_label["text"] = self.data_text
        self.data_label.config(font=labelfont, bg = label_bg, fg = label_fg)

        self.QUIT_button.pack({"side": "left", "expand": "YES", "fill": "both"})
        self.start_rec_button.pack({"side": "left", "expand": "YES", "fill": "both"})
        self.choose_dir_button.pack({"side": "left", "expand": "YES", "fill": "both"})
        self.set_depth_buton.pack({"side": "top", "expand": "YES", "fill": "both"})
        self.reset_depth_button.pack({"side": "bottom", "expand": "YES", "fill": "both"})
        self.data_label.pack({"side": "left", "expand":"YES", "fill":"both"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.data_text = "INITIALIZE"
        self.pack()
        self.createWidgets()



