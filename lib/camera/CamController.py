"""
Camera control panel module, that provides tools for
changing directory, setting up time, start and stop recording
and formatting SD card
"""

import requests
from lib.UI.Settings import Settings

class CameraContoller:

    def __init__(self, settings : Settings):
        self.URL = settings.camera_settings.URL
        self.login = settings.camera_settings.login
        self.password = settings.camera_settings.password
        self.folder = settings.default_folder

    def connectCamera(self):
        pass