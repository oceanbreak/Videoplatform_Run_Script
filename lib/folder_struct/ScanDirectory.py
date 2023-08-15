"""
Module to scan directory and creating auxiliary files in it
when video is recorder or photo  is taken.
"""

from lib.data.SonarThread import SonarThread
from lib.folder_struct.SrtGenerator import SrtGenerator
from lib.folder_struct.ImageCaption import ImageCaption
from lib.data.DataCollection import DataCollection
from tkinter import Tk
import os
from threading import Thread


class ScanDirectory:

    # Enumerates
    IMAGE = 1
    VIDEO = 2

    def __init__(self, folder, data_collection : DataCollection):
        self.data_collection = data_collection
        self.__scan_folder = folder
        self.__cur_file_list = self.getFileList()
        self.image_extension_list = ('jpg', 'JPG', 'png', 'PNG')
        self.video_extension_list = ('avi', 'AVI', 'mp4', 'MP4')
        self.image_flag = None
        self.video_flag = None


    def getFileList(self):
        return os.popen('dir "' + self.__scan_folder + '" /B').readlines()
    

    def getAddedItem(self):
        new_file_list = self.getFileList()
        if len(new_file_list) > len(self.__cur_file_list):
            new_items = [item.rstrip() for item in new_file_list if item not in self.__cur_file_list]
            for new_item in new_items:
                self.newItemFlag(new_item)
            self.__cur_file_list = new_file_list
        else:
            self.__cur_file_list = new_file_list

        
    def newItemFlag(self, item):
        full_path = os.path.join(self.__scan_folder, item)
        if item[-3:] in self.image_extension_list:
            print(f'Image {item} added')
            snap = ImageCaption(full_path, self.data_collection)
            snap.addCaption()
            snap.addSnapLogLine()
        
        elif item[-3:] in self.video_extension_list:
            print(f'Video {item} added')
            srt = SrtGenerator(full_path, self.data_collection)
            srt_proc = Thread(None, srt.generateSrtFile)
            srt_proc.start()
            self.video_flag = item

    def resetFlags(self):
        self.image_flag = None
        self.video_flag = None
        

        


if __name__ == '__main__':
    scaner = ScanDirectory('D:/')
    try:
        while True:
            scaner.getAddedItem()

    finally:
        print('End')