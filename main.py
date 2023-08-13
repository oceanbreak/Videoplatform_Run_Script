################################################
###                                          ###
###  SONARLAB's OceanRecord software         ###
###  for communication with TUV Videomodule  ###
###  designed in Sonarlab                    ###
###  Shirshov Institute of Oceanology        ###
###  Russian Academy of Science              ###
###                                          ###
################################################

from lib.UI.UI_interface import MainWindow, SettingsWindow
from lib.UI.Settings import Settings

class MainApplication:

    def __init__(self):
        self.__global_settings = Settings()
        self.__global_settings.readSettingsFromFile()
        self.__mainUI = MainWindow()
        self.setupMainAppButtons()
        self.__mainUI.mainloop()


    def setupMainAppButtons(self):
        self.__mainUI.connect_button['command'] = self.connect_button_command
        self.__mainUI.settings_button['command'] = self.settings_button_command


    def setupSettingsWindowButtons(self):
        self.settings_window.apply_button['command'] = self.readSettingsFromUI
        self.__global_settings.writeSettings()


    def connect_button_command(self):
        print('Conncecting')

    
    def readSettingsFromUI(self):
        self.__global_settings.readSettingsFromUI(self.settings_window)

    
    def settings_button_command(self):
        self.settings_window = self.__mainUI.settingsWindow()
        self.__global_settings.putSettingsToUI(self.settings_window)
        self.setupSettingsWindowButtons()


if __name__ == '__main__':
    MainApplication()