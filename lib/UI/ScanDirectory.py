"""
Module to scan directory and creating auxiliary files in it
when video is recorder or photo  is taken
"""

from threading import Thread
import os

# Enumerates
IMAGE = 1
VIDEO = 2

class ScanDirectory:

    def __init__(self, folder):
        self.__scan_folder = folder
        self.__cur_file_list = self.getFileList()
        self.image_extension_list = ('jpg', 'JPG', 'png', 'PNG')
        self.video_extension_list = ('avi', 'AVI', 'mp4', 'MP4')

    def getFileList(self):
        return os.popen('dir "' + self.__scan_folder + '" /B').readlines()
    
    def getAddedItem(self):
        new_file_list = self.getFileList()
        if len(new_file_list) > len(self.__cur_file_list):
            new_item = [item.rstrip() for item in new_file_list if item not in self.__cur_file_list][0]
            self.__cur_file_list = new_file_list
            return (self.newItemFlag(new_item), new_item)
        else:
            self.__cur_file_list = new_file_list
            return None
        
    def newItemFlag(self, item):
        if item[-3:] in self.image_extension_list:
            return IMAGE
        else:
            return None
    


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

if __name__ == '__main__':
    scaner = ScanDirectory('D:/')
    try:
        while True:
            ret = scaner.getAddedItem()
            if ret is not  None:
                print(ret)

    finally:
        print('End')