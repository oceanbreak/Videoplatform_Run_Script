"""
Camera control panel module, that provides tools for
changing directory, setting up time, start and stop recording
and formatting SD card
"""

import requests
from lib.UI.Settings import Settings
import datetime
from urllib import request

class CameraContoller:

    def __init__(self, settings : Settings):
        self.URL = settings.camera_settings.URL
        self.login = settings.camera_settings.login
        self.password = settings.camera_settings.password
        self.folder = settings.default_folder
        self.auth = (self.login, self.password)

        self.__connected = False


    def connected(self):
        return self.__connected


    def checkConnection(self):
        try:
            request.urlopen(self.URL, timeout=1)
            return True
        except:
            return  False

    def connectCamera(self):
        print('Connecting')
        if not self.checkConnection():
            return False
        cam_req = requests.get(self.URL + '/cgi-bin/capture.cgi?action=set&capture_folder='
                            + self.folder, auth=self.auth)
        if cam_req.status_code == 200:
            print(f'Camera connected\nRecord folder: {self.folder}')
            self.__connected = True
            return True
        else:
            print('Cannot connect to camera')
            return False


    def disconnectCamera(self):
        self.__connected = False
        print('Camera disconnected')


    def startRecSD(self):
        if self.__connected:
            resp5 = requests.get(self.URL + '/cgi-bin/admin/param.cgi?action=update' \
                        '&Recording.R0.Enabled=yes&Recording.R0.Weekdays=1111111', auth = self.auth)
            print(resp5.content.decode('utf-8'))


    def stopRecSD(self):
        if self.__connected:
            resp6 = requests.get(self.URL + '/cgi-bin/admin/param.cgi?action=update' \
                     '&Recording.R0.Enabled=no&Recording.R0.Weekdays=0000000', auth = self.auth)
            print(resp6.content.decode('utf-8'))


    def syncTime(self):
        now = datetime.now()
        HH, MM, SS, DT, MN, YY = (now.hour,
                                now.minute,
                                now.second + 3,
                                now.day,
                                now.month,
                                now.year)

        message = '/cgi-bin/admin/date.cgi?action=set&year=%i&month=%i&day=%i' \
                    '&hour=%i&minute=%i&second=%i' % (YY, MN, DT, HH, MM, SS)

        resp3 = requests.get(self.URL + message, auth = self.auth)
        print(resp3.content.decode('utf-8'))


    def formatSD(self):
        resp2 = requests.get(self.URL + '/cgi-bin/admin/storagemanagement.cgi?action=format', auth = self.auth)
        print(resp2.content)
