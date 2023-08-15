################################################
###                                          ###
###  SONARLAB's OceanRecord software         ###
###  for communication with TUV Videomodule  ###
###  designed in Sonarlab                    ###
###  Shirshov Institute of Oceanology        ###
###  Russian Academy of Science              ###
###                                          ###
################################################

import lib.UI.UI_interface as UI_Interface
from lib.UI.Settings import Settings
from lib.data.DataCollection import DataCollection, DataPacket
from lib.Utils import textShorten
from lib.data.BufferGenerator import *
from lib.calculations.TrackCounter import TrackCounter
from lib.folder_struct.ScanDirectory import ScanDirectory
from lib.data.SonarThread import SonarThread

class MainApplication:

    def __init__(self):
        

        self.data_collection = DataCollection()
        self.global_settings = Settings()
        self.track_counter = TrackCounter()

        self.root = UI_Interface.Tk.Tk()
        self.mainUI = UI_Interface.MainWindow(self.root)
        self.mainUI.master.title('OceanRecord')

        # Paramteres
        self.update_text_frequency = 100
        self.track_calculation_freq = 100

        # FLAGS
        self.__is_running = False
        self.__is_recording = False



        try:
            self.global_settings.readSettingsFromFile()
        except (FileNotFoundError, ValueError):
            self.mainUI.popUpWarning('No settings file found')

        print(self.global_settings)
            

        self.setupMainAppButtons()
        self.mainUI.mainloop()

############### SETIP UI ELEMENTS #######################################

    def setupMainAppButtons(self):
        self.mainUI.connect_button['command'] = self.connect_button_command
        self.mainUI.settings_button['command'] = self.settings_button_command
        self.mainUI.QUIT_button['command'] = self.quit_button_command
        self.mainUI.cam_dialog_button['command'] = self.cam_button_command
        self.mainUI.set_depth_buton['command'] = self.set_depth_button_command
        self.mainUI.start_rec_button['command'] = self.start_button_command
        self.mainUI.reset_track_button['command'] = self.reset_track_command
        # self.mainUI.choose_dir_button['text'] = textShorten(self.global_settings.default_folder)


    def setupSettingsWindowButtons(self):
        self.settings_window.apply_button['command'] = self.readSettingsFromUI
        

    def connect_button_command(self):
        self.mainUI.updateDataText('Connecting...')
        self.mainUI.setButtonsActive()
        self.mainUI.connect_button['text'] = 'Disconnect'
        self.mainUI.connect_button['command'] = self.disconnect_button_command

        try:
            self.buffers = BufferCollection(self.global_settings)
            self.buffers.InnitiateBuffers()
            self.__is_running = True
            self.updateData()
            self.updateDisplay()
        except AttributeError:
            self.disconnect_button_command()


    def disconnect_button_command(self):
        self.__is_running = False
        self.buffers.stopWritingBuffers()
        self.mainUI.updateDataText('Welcome to Sonarlab')
        self.mainUI.setButtonsInactive()
        self.mainUI.connect_button['text'] = 'Connect'
        self.mainUI.connect_button['command'] = self.connect_button_command

    
    def settings_button_command(self):
        self.settings_window = self.mainUI.settingsWindow()
        self.putSettingsToUI()
        self.setupSettingsWindowButtons()


    def quit_button_command(self):
        if self.__is_running:
            self.buffers.stopWritingBuffers()
        self.mainUI.quit()


    def cam_button_command(self):
        self.cam_control_window = self.mainUI.camControlWindow()


    def set_depth_button_command(self):
        self.buffers.sendMessage('DEPTH', b'set 0')
        # self.buffer_queue[1].send_message(b'set 0')


    def start_button_command(self):
        print('Im in rec buttton')
        self.__is_recording = True
        self.track_counter.initTrackTimer()
        self.mainUI.start_rec_button.config(text='Stop', fg='red', command=self.stop_button_connamd)
        self.scanDirectory()
        self.calculateTrack()



    def stop_button_connamd(self):
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

        self.global_settings.inclin_port.port = self.settings_window.chan5_port.get()
        self.global_settings.inclin_port.rate = int(self.settings_window.chan5_rate.get())
        self.global_settings.inclin_port.enable = self.settings_window.chan5_active.get()

        self.global_settings.writeSettings()
        self.data_collection.clear()
        print("New settings written to file")

    
    def updateData(self):
        if self.__is_running:
            raw_data = self.buffers.getRawData()
            self.data_collection.readDataFromBuffer(raw_data)
            self.mainUI.after(self.update_text_frequency, self.updateData)

    
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

        


if __name__ == '__main__':
    MainApplication()