import lib.UI.UI_interface as UI_Interface
from lib.UI.Settings import Settings
from lib.data.DataCollection import DataCollection, DataPacket
from lib.Utils import textShorten
from lib.data.BufferGenerator import *
from lib.calculations.TrackCounter import TrackCounter
from lib.folder_struct.ScanDirectory import ScanDirectory
from lib.data.SonarThread import SonarThread
from lib.folder_struct.LogFileGenerator import LogFileGeneraror
from lib.camera.CamController import CameraContoller
from tkinter.filedialog import askdirectory
from lib.folder_struct.SrtFromLog import SrtFromLog
from threading import Thread
from lib.data.Graphs import Graphs

#TODO Cancel button for downloading

def threadDecorator(function):
    def wrapper(*args):
        t_func = Thread(None, function, args=args)
        t_func.start()
    return wrapper

class MainApplication:

    def __init__(self):
    
        
        self.global_settings = Settings()
        

        self.root = UI_Interface.Tk.Tk()
        self.mainUI = UI_Interface.MainWindow(self.root)
        self.mainUI.master.title('Ocean Record')
        self.root.geometry('530x400')
        self.root.wm_iconbitmap('resources/OceanRecIcon.ico')

        # Paramteres
        self.update_text_frequency = 200
        self.track_calculation_freq = 200

        # FLAGS
        self.__is_running = False
        self.__is_recording = False
        self.__is_downloading = False

        # Read settings
        try:
            self.global_settings.readSettingsFromFile()
        except (FileNotFoundError, ValueError):
            self.mainUI.popUpWarning('No settings file found. Creating')

        print(self.global_settings)

        self.data_collection = DataCollection(self.global_settings)
        self.track_counter = TrackCounter()
        self.camera_control = CameraContoller(self.global_settings)
            
        
        self.setupMainAppButtons()

        # Double function of quit button
        self.root.protocol('WM_DELETE_WINDOW', self.quit_button_command)
        # self.mainUI.mainloop()

############### SETIP UI ELEMENTS #######################################

    def setupMainAppButtons(self):
        self.mainUI.connect_button['command'] = self.connect_button_command
        self.mainUI.settings_button['command'] = self.settings_button_command
        self.mainUI.QUIT_button['command'] = self.quit_button_command
        self.mainUI.cam_dialog_button['command'] = self.cam_button_command
        self.mainUI.set_depth_buton['command'] = self.set_depth_button_command
        self.mainUI.start_rec_button['command'] = self.start_button_command
        self.mainUI.reset_track_button['command'] = self.reset_track_command
        self.mainUI.srt_from_log_button['command'] = self.srt_from_log_command
        self.mainUI.plot_graphs_button['command'] = self.plot_graphs_command
        # self.mainUI.choose_dir_button['text'] = textShorten(self.global_settings.default_folder)


    def setupSettingsWindowButtons(self):
        self.settings_window.apply_button['command'] = self.readSettingsFromUI
        self.settings_window.default_folder_button['command'] = self.choose_folder_command


    def choose_folder_command(self):
        new_folder = askdirectory(initialdir=self.global_settings.default_folder)
        if new_folder == '': return
        self.global_settings.default_folder = new_folder
        self.settings_window.default_folder_button['text'] = textShorten(new_folder)

        # Update camera directory, if camera connected
        if hasattr(self, 'cam_control'):
            print('Trying to change cam folder')
            self.camera_control.folder = new_folder

    def srt_from_log_command(self):
        self.log_reader = SrtFromLog(self.global_settings, self.data_collection)
        ret = self.log_reader.run()
        if ret:
            video_list = self.log_reader.video_list
            text = 'Successfully created SRT for videos:\n' + \
                    '\n'.join(video_list)
            self.mainUI.popInfo(text)

    def plot_graphs_command(self):
        self.grapher = Graphs(self.data_collection, self.global_settings)
        self.grapher.run()
        

    def connect_button_command(self):
        self.mainUI.cearImageOnLabel()
        self.mainUI.updateDataText('Connecting...')
        self.mainUI.setButtonsActive()
        self.mainUI.connect_button['text'] = 'Disconnect'
        self.mainUI.connect_button['command'] = self.disconnect_button_command
        

        try:
            self.buffers = BufferCollection(self.global_settings)
            self.buffers.InnitiateBuffers()
            self.__is_running = True
            self.updateData()
            self.updateTime()
            self.updateDisplay()
        except AttributeError:
            self.disconnect_button_command()


    def disconnect_button_command(self):
        if self.__is_recording:
            yes = self.mainUI.popAskWindow('Log-file writing in process. Stop?')
            if not yes: return
            self.stop_button_command()
        self.__is_running = False
        self.buffers.stopWritingBuffers()
        self.mainUI.updateDataText('')
        self.mainUI.setupImageOnLabel()
        self.mainUI.setButtonsInactive()
        self.mainUI.connect_button['text'] = 'Connect'
        self.mainUI.connect_button['command'] = self.connect_button_command


    
    def settings_button_command(self):
        self.settings_window = self.mainUI.settingsWindow()
        self.putSettingsToUI()
        self.setupSettingsWindowButtons()


    def quit_button_command(self):
        yes = self.mainUI.popAskWindow('Quit program?')
        if yes:
            if self.__is_recording:
                self.stop_button_command()
            if self.__is_running:
                self.buffers.stopWritingBuffers()
            self.mainUI.quit()


    def cam_button_command(self):
        self.cam_control_window = self.mainUI.camControlWindow()
        self.setupCameraButtons()


    def set_depth_button_command(self):
        self.buffers.sendMessage('DEPTH', b'set 0')
        # self.buffer_queue[1].send_message(b'set 0')


    def start_button_command(self):
        print('Im in rec buttton')
        self.__is_recording = True
        self.logWriter = LogFileGeneraror(self.global_settings.default_folder, self.data_collection)
        self.track_counter.initTrackTimer()
        self.mainUI.start_rec_button.config(text='Stop', fg='red', command=self.stop_button_command)
        self.scanDirectory()
        self.calculateTrack()
        self.generateLogFile()



    def stop_button_command(self):
        self.mainUI.start_rec_button.config(text='Start', fg='dark green', command=self.start_button_command)
        # self.track_counter.resetTrack()
        self.__is_recording = False
        self.scan_dir_thread.stop()


    def reset_track_command(self):
        if not self.__is_recording:
            self.track_counter.resetTrack()
            self.data_collection.track_length = DataPacket(self.track_counter.getCurTrackLength())
            self.data_collection.track_time_length = DataPacket(self.track_counter.getCurTrackTime())
            print('Track reset')


############### CAMERA WINDOW @@@@@@@@@@@@@@@@@@@@@@@@2

    def setupCameraButtons(self):

        if self.camera_control.connected():
            self.cam_control_window.activateButtons()
            self.cam_control_window.connect_button['text'] = 'Disconnect camera'
            self.displayVideoList()

        self.cam_control_window.connect_button['command'] = self.connect_camera_command
        self.cam_control_window.sync_time_button['command'] = self.sync_time_command
        self.cam_control_window.format_sd_button['command'] = self.format_sd_command
        self.cam_control_window.rec_sd_button['command'] = self.cam_rec_command
        self.cam_control_window.download_button['command'] = self.download

        if self.camera_control.recording():
            self.cam_control_window.rec_sd_button['text'] = 'Stop SD rec'
            self.cam_control_window.rec_sd_button['fg'] = 'red'
        

    @threadDecorator
    def sync_time_command(self):
        self.camera_control.syncTime()
        self.cam_control_window.insertDisplayText(f'Camera time set {self.data_collection.datetime.data.toDisplayText()}')

    @threadDecorator
    def connect_camera_command(self):
        # print('Am i connecting')
        if not self.camera_control.connected():
            success = self.camera_control.connectCamera()
            time.sleep(0.2)
            if success:
                self.setupCameraButtons()
                self.cam_control_window.connect_button['text'] = 'Disconnect camera'
                self.displayVideoList()
                # self.setupCameraButtons()
                self.cam_control_window.activateButtons()

            else:
                self.mainUI.popError('Cannot connect to camera')
        else:
            self.camera_control.disconnectCamera()
            self.cam_control_window.deactivateButtons()
            self.cam_control_window.connect_button['text'] = 'Connect camera'
            self.cam_control_window.insertDisplayText('Camera is not connected')

        # self.setupCameraButtons()


    @threadDecorator
    def format_sd_command(self):
        yes = self.mainUI.popAskWindow('Format SD?\nThat will erase all data on camera')
        if yes:
            self.camera_control.formatSD()
            self.mainUI.after(5000, self.displayVideoList)
    

    @threadDecorator
    def cam_rec_command(self):
        if self.camera_control.recording():
            self.camera_control.stopRecSD()
            self.cam_control_window.rec_sd_button['text'] = 'Start SD rec'
            self.cam_control_window.rec_sd_button['fg'] = 'black'
            print('Camera stopped record')
        else:
            self.camera_control.startRecSD()
            self.cam_control_window.rec_sd_button['text'] = 'Stop SD rec'
            self.cam_control_window.rec_sd_button['fg'] = 'red'
            print('Camera started recording')
        self.displayVideoList()


    @threadDecorator
    def displayVideoList(self):
        if self.camera_control.connected():
            v_list = self.camera_control.listVideos()
            self.cam_control_window.insertDisplayText('\n'.join(v_list))


    @threadDecorator
    def download(self):
        if self.camera_control.connected():
            self.__is_downloading = True
            self.cam_control_window.download_button['command'] = self.cancel_download
            self.updateDownloadBar()
            self.cam_control_window.disableAll()

            self.camera_control.download()
            
            self.mainUI.popInfo('Download complete')
            self.__is_downloading = False
            self.cam_control_window.enableAll()
            self.camera_control.eraseDowloadProgress()

            # Reset download bar
            self.cam_control_window.download_file_label['text'] = ''
            self.cam_control_window.progress_complete.set(self.camera_control.download_progress)


    def cancel_download(self):
        self.camera_control.stopDownload()
        self.cam_control_window.download_button['command'] = self.download


    def updateDownloadBar(self):
        if self.__is_downloading:
            # print(self.camera_control.cur_download_filename, self.camera_control.download_progress)
            text = f'Downloading {self.camera_control.cur_download_filename}'
            self.cam_control_window.download_file_label['text'] = text
            self.cam_control_window.progress_complete.set(self.camera_control.download_progress)
            self.mainUI.after(100, self.updateDownloadBar)


    # def updateVideoList(self):
    #     print(f'Camera connected: {self.camera_control.connected()}')
    #     # Update video list when recording
    #     self.displayVideoList()
    #     self.mainUI.after(10000, self.updateVideoList)



################# PROGRAM LOGIC #################################

    def putSettingsToUI(self):
        """
        Translates all read settings into settings window
        """

        # NAVI
        self.settings_window.chan1_port.insert(0, self.global_settings.navi_port.port)
        self.settings_window.chan1_rate.insert(0, str(self.global_settings.navi_port.rate))
        self.settings_window.chan1_message.insert(0, self.global_settings.navi_port.message)
        self.settings_window.chan1_atctivator.deselect() if not self.global_settings.navi_port.enable \
                                                    else self.settings_window.chan1_atctivator.select()
        # DEPTH
        self.settings_window.chan2_port.insert(0, self.global_settings.depth_port.port)
        self.settings_window.chan2_rate.insert(0, str(self.global_settings.depth_port.rate))
        self.settings_window.chan2_message.insert(0, self.global_settings.depth_port.message)
        self.settings_window.chan2_atctivator.deselect() if not self.global_settings.depth_port.enable \
                                                    else self.settings_window.chan2_atctivator.select()
        # ALT
        self.settings_window.chan3_port.insert(0, self.global_settings.altimeter_port.port)
        self.settings_window.chan3_rate.insert(0, str(self.global_settings.altimeter_port.rate))
        self.settings_window.chan3_message.insert(0, self.global_settings.altimeter_port.message)
        self.settings_window.chan3_atctivator.deselect() if not self.global_settings.altimeter_port.enable \
                                                    else self.settings_window.chan3_atctivator.select()
        # TEMP
        self.settings_window.chan4_port.insert(0, self.global_settings.temp_port.port)
        self.settings_window.chan4_rate.insert(0, str(self.global_settings.temp_port.rate))
        self.settings_window.chan4_message.insert(0, self.global_settings.temp_port.message)
        self.settings_window.chan4_atctivator.deselect() if not self.global_settings.temp_port.enable \
                                                    else self.settings_window.chan4_atctivator.select()
        
        # SONAR
        self.settings_window.chan6_port.insert(0, self.global_settings.sonar_port.port)
        self.settings_window.chan6_rate.insert(0, str(self.global_settings.sonar_port.rate))
        self.settings_window.chan6_message.insert(0, self.global_settings.sonar_port.message)
        self.settings_window.chan6_atctivator.deselect() if not self.global_settings.sonar_port.enable \
                                                    else self.settings_window.chan6_atctivator.select()
        
        # INCLIN
        self.settings_window.chan5_port.insert(0, self.global_settings.inclin_port.port)
        self.settings_window.chan5_rate.insert(0, str(self.global_settings.inclin_port.rate))
        self.settings_window.chan5_atctivator.deselect() if not self.global_settings.inclin_port.enable \
                                                    else self.settings_window.chan5_atctivator.select()
        

        # CAMERA
        self.settings_window.cam_IP_entry.insert(0, self.global_settings.camera_settings.URL)
        self.settings_window.cam_login_entry.insert(0, self.global_settings.camera_settings.login)
        self.settings_window.cam_password_entry.insert(0, self.global_settings.camera_settings.password)

        # Folder
        self.settings_window.default_folder_button['text'] = textShorten(self.global_settings.default_folder)

        # Common
        self.settings_window.log_file_freq_entry.insert(0, self.global_settings.log_write_freq)
        self.settings_window.UTC_activator.deselect() if not self.global_settings.UTC_time \
                                                    else self.settings_window.UTC_activator.select()


    def readSettingsFromUI(self):
        
        self.global_settings.navi_port.port = self.settings_window.chan1_port.get()
        self.global_settings.navi_port.rate = int(self.settings_window.chan1_rate.get())
        self.global_settings.navi_port.message = self.settings_window.chan1_message.get()
        self.global_settings.navi_port.enable = self.settings_window.chan1_active.get()

        self.global_settings.depth_port.port = self.settings_window.chan2_port.get()
        self.global_settings.depth_port.rate = int(self.settings_window.chan2_rate.get())
        self.global_settings.depth_port.message = self.settings_window.chan2_message.get()
        self.global_settings.depth_port.enable = self.settings_window.chan2_active.get()

        self.global_settings.altimeter_port.port = self.settings_window.chan3_port.get()
        self.global_settings.altimeter_port.rate = int(self.settings_window.chan3_rate.get())
        self.global_settings.altimeter_port.message = self.settings_window.chan3_message.get()
        self.global_settings.altimeter_port.enable = self.settings_window.chan3_active.get()

        self.global_settings.temp_port.port = self.settings_window.chan4_port.get()
        self.global_settings.temp_port.rate = int(self.settings_window.chan4_rate.get())
        self.global_settings.temp_port.message = self.settings_window.chan4_message.get()
        self.global_settings.temp_port.enable = self.settings_window.chan4_active.get()

        self.global_settings.sonar_port.port = self.settings_window.chan6_port.get()
        self.global_settings.sonar_port.rate = int(self.settings_window.chan6_rate.get())
        self.global_settings.sonar_port.message = self.settings_window.chan6_message.get()
        self.global_settings.sonar_port.enable = self.settings_window.chan6_active.get()

        self.global_settings.inclin_port.port = self.settings_window.chan5_port.get()
        self.global_settings.inclin_port.rate = int(self.settings_window.chan5_rate.get())
        self.global_settings.inclin_port.enable = self.settings_window.chan5_active.get()

        # Cam
        self.global_settings.camera_settings.URL = self.settings_window.cam_IP_entry.get()
        self.global_settings.camera_settings.login = self.settings_window.cam_login_entry.get()
        self.global_settings.camera_settings.password = self.settings_window.cam_password_entry.get()

        self.global_settings.log_write_freq = int(self.settings_window.log_file_freq_entry.get())
        self.global_settings.UTC_time = int(self.settings_window.UTC_active.get())

        self.global_settings.writeSettings()
        self.data_collection.clear()
        print("New settings written to file")

    
    def updateData(self):
        if self.__is_running:
            # print('updating buffer')
            raw_data = self.buffers.getRawData()
            self.data_collection.readDataFromBuffer(raw_data)
            self.mainUI.after(self.update_text_frequency, self.updateData)

    def updateTime(self):
        if self.__is_running:
            # print('Updating time')
            self.data_collection.updateTime()
            self.mainUI.after(1000, self.updateTime)

    
    def updateDisplay(self):
        # Main display of a program
        if self.__is_running:
            self.mainUI.data_label['text'] = self.data_collection.toDisplayText()
            self.mainUI.after(self.update_text_frequency, self.updateDisplay)


    def calculateTrack(self):
        if self.__is_recording:
            try:
                self.track_counter.incrementTime()
                self.data_collection.track_time_length = DataPacket(self.track_counter.getCurTrackTime())
                self.track_counter.incrementTrack(self.data_collection.navi_data.data)
                self.data_collection.track_length = DataPacket(self.track_counter.getCurTrackLength())
                
            except AttributeError:
                print( 'Error in track data')

            finally:
                self.mainUI.after(self.track_calculation_freq, self.calculateTrack)


    def scanDirectory(self):
        scan_dir = ScanDirectory(self.global_settings.default_folder, self.data_collection)
        self.scan_dir_thread = SonarThread(scan_dir.getAddedItem)
        self.scan_dir_thread.start()

        # if self.__is_recording:
        #     self.scan_dr_process.getAddedItem()
        #     self.mainUI.after(self.update_text_frequency, self.scanDirectory)

    def generateLogFile(self):
        if self.__is_recording:
            # print('Writing log file')
            self.logWriter.writeLogString()
            self.mainUI.after(self.global_settings.log_write_freq*1000, self.generateLogFile)

        

