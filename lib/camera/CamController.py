"""
Camera control panel module, that provides tools for
changing directory, setting up time, start and stop recording
and formatting SD card
"""

import requests
from lib.UI.Settings import Settings
import datetime
from urllib import request
from requests.exceptions import ConnectTimeout

class CameraContoller:

    def __init__(self, settings : Settings):
        self.URL = settings.camera_settings.URL
        self.login = settings.camera_settings.login
        self.password = settings.camera_settings.password
        self.folder = settings.default_folder
        self.auth = (self.login, self.password)

        self.__connected = False
        self.__recording = False


    def connected(self):
        return self.__connected
    

    def recording(self):
        return self.__recording


    def checkConnection(self):
        try:
            print(self.URL)
            request.urlopen(self.URL, timeout=5)
            return True
        except ValueError:
            return  False

    def connectCamera(self):
        print('Connecting')
        # if not self.checkConnection():
        #     return False
        try:
            cam_req = requests.get(self.URL + '/cgi-bin/capture.cgi?action=set&capture_folder='
                                + self.folder, auth=self.auth, timeout=2)
            if cam_req.status_code == 200:
                print(f'Camera connected\nRecord folder: {self.folder}')
                self.__connected = True
                if self.requestIfRecoring():
                    self.__recording = True
                return True
            
            else:
                print('Cannot connect to camera')
                return False
        except (ConnectionError, ConnectTimeout):
            return False


    def disconnectCamera(self):
        self.__connected = False
        print('Camera disconnected')


    def startRecSD(self):
        if self.__connected:
            resp5 = requests.get(self.URL + '/cgi-bin/admin/param.cgi?action=update' \
                        '&Recording.R0.Enabled=yes&Recording.R0.Weekdays=1111111', auth = self.auth)
            print(resp5.content.decode('utf-8'))
            self.__recording = True


    def stopRecSD(self):
        if self.__connected:
            resp6 = requests.get(self.URL + '/cgi-bin/admin/param.cgi?action=update' \
                     '&Recording.R0.Enabled=no&Recording.R0.Weekdays=0000000', auth = self.auth)
            print(resp6.content.decode('utf-8'))
            self.__recording = False


    def syncTime(self):
        now = datetime.datetime.now()
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


    def listParameters(self):
        # List parameters
        resp4 = requests.get(self.URL + '/cgi-bin/admin/param.cgi?action=list', auth = self.auth)
        return resp4.content.decode('utf-8').split('\n')
    

    def requestIfRecoring(self):
        for parameter in self.listParameters():
            if 'root.Recording.R0.Enabled' in parameter:
                _, value = parameter.split('=')
                if value == 'no':
                    return False
                if value =='yes':
                    return True
        return False