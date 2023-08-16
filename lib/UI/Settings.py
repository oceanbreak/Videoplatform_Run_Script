""" Module that works with settings.xml files for sonar programs"""

import sys
import xml.etree.ElementTree as ET
from lib.data.DataStructure import data_keywords
from lib.UI.UI_interface import SettingsWindow

#TODO Добавить частоту записи данныз в лог-файл.

class ComPortSettings:
    """
    Class that describes com port block in cnfig file:
    ####_ENBL = 1 / 0
    ####_PORT = COM##
    ####_RATE = #####
    ####_MESSAGE = #####
    """

    def __init__(self, keyword=''):
        self.enable = 0
        self.port = ''
        self.rate = 0
        self.message = ''
        self.keyword = keyword

    def is_enabled(self):
        return self.enable

    def set_port(self, index : int):
        self.port = f'COM{index}'

    def set_rate(self, rate : int):
        self.rate = rate

    def set_message(self, message : str):
        self.message = message

    def enable_as_str(self):
        return "ON" if self.enable else "OFF"

    def __str__(self):
        return f"{self.enable_as_str()}, {self.port}, Baud rate={self.rate}, NMEA message={self.message}\n"


class CameraSettings:

    def __init__(self):
        self.URL = ''
        self.login = ''
        self.password = ''

    def __str__(self):
        return f'URL: {self.URL}, login: {self.login}, password: {self.password}\n'


class Settings:
    """
    Class that works with init.cfg file
    """
    def __init__(self):
        self.navi_port = ComPortSettings(data_keywords.NAVI)
        self.depth_port = ComPortSettings(data_keywords.DEPTH)
        self.altimeter_port = ComPortSettings(data_keywords.ALTIMETER)
        self.inclin_port = ComPortSettings(data_keywords.INCLIN)
        self.temp_port = ComPortSettings(data_keywords.TEMP)
        self.sonar_port = ComPortSettings(data_keywords.SONAR)
        self.camera_settings = CameraSettings()
        self.default_folder = ''
        self.log_write_freq = 1
        self.UTC_time = 1
        self.config_file = 'resources/settings.xml'

    def __str__(self):
        return "SETTINGS:\n" + \
                "COM ports:\n" + \
                'NAVI: ' + str(self.navi_port) + \
                'DEPTH: ' +str(self.depth_port) + \
                'ALT: ' +str(self.altimeter_port) + \
                'INCLIN: ' +str(self.inclin_port) + \
                'TEMP: ' +str(self.temp_port) + \
                'SONAR: ' +str(self.sonar_port) + \
                "Camera settings:\n" + \
                str(self.camera_settings) + \
                f"Default rec folder: {self.default_folder}\n" + \
                f"Log file writing frequency: {self.log_write_freq} s\n" + \
                f"Time in UTC: {'YES' if self.UTC_time else 'NO'}"

    def ports_as_array(self):
        return (self.navi_port,
                self.depth_port,
                self.altimeter_port,
                self.inclin_port,
                self.temp_port,
                self.sonar_port)


    def readSettingsFromFile(self):
        # Read settings from XML file
        tree = ET.parse(self.config_file)
        root = tree.getroot()

        # Read COM-ports
        for chan in root.iter('channel'):
            for keyword, port_obj in zip(data_keywords.as_array, self.ports_as_array()):
                if chan.attrib['id'] == keyword:
                    port_obj.keyword = keyword
                    port_obj.enable = int(chan[0].text)
                    port_obj.port = str(chan[1].text)
                    port_obj.rate = int(chan[2].text)
                    port_obj.message = str(chan[3].text)

        # Read common settings
        for item in root.iter('common'):
            self.default_folder = item[0].text
            self.log_write_freq = int(item[1].text)
            self.UTC_time = int(item[2].text)

        # Read IP Camera settingds
        for item in root.iter('IP_camera'):
            self.camera_settings.URL = item[0].text
            self.camera_settings.login = item[1].text
            self.camera_settings.password = item[2].text

    
    def writeSettings(self):
        # Write Settings structure to XML file

        settings = ET.Element('settings')

        # Common settings
        common = ET.SubElement(settings, 'common')
        default_folder = ET.SubElement(common, 'folder')
        default_folder.text = self.default_folder
        log_freq = ET.SubElement(common, 'log_freq')
        log_freq.text = str(self.log_write_freq)
        UTC_time = ET.SubElement(common, 'UTC')
        UTC_time.text = str(self.UTC_time)

        # COM port settings
        channels = ET.SubElement(settings, 'channels')

        for port_object in self.ports_as_array():
            channel = ET.SubElement(channels, 'channel')
            channel.set('id', port_object.keyword)
            enabled = ET.SubElement(channel, "enabled")
            enabled.text = str(port_object.enable)
            serial = ET.SubElement(channel, 'serial')
            serial.text = str(port_object.port)
            rate = ET.SubElement(channel, 'baud_rate')
            rate.text = str(port_object.rate)
            message = ET.SubElement(channel, 'message')
            message.text = str(port_object.message)

        # Camera settings
        camera = ET.SubElement(settings, 'IP_camera')
        URL_link = ET.SubElement(camera, 'URL')
        URL_link.text = self.camera_settings.URL
        login = ET.SubElement(camera, 'login')
        login.text = self.camera_settings.login
        password = ET.SubElement(camera, 'password')
        password.text = self.camera_settings.password

        # Generate XML string
        b_xml = ET.tostring(settings, encoding="unicode")

        with open('resources/settings.xml', 'w') as f_write:
            f_write.write(b_xml)




if __name__ == '__main__':
    
    # settings = Settings()
    # a = settings.readInitParamsictionary()
    # print(a)
    # Test XML settings view

    tree = ET.parse('resources/settings.xml')
    root = tree.getroot()
    print(root.tag)

    for child in root:
        print(child.tag, child.attrib)
