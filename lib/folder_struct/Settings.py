""" Module that works with init.cfg files for sonar programs"""

import sys
import xml.etree.ElementTree as ET
from lib.data.DataStructure import data_keywords

class ComPortSettings:
    """
    Class that describes com port block in cnfig file:
    ####_ENBL = 1 / 0
    ####_PORT = COM##
    ####_RATE = #####
    ####_MESSAGE = #####
    """

    def __init__(self):
        self.enable = False
        self.port = None
        self.rate = None
        self.message = None

    def enable(self):
        self.enable = True

    def disable(self):
        self.enable = False

    def is_enabled(self):
        return self.enable

    def set_port(self, index : int):
        self.port = f'COM{index}'

    def set_rate(self, rate : int):
        self.rate = rate

    def set_message(self, message : str):
        self.message = message


class CameraSettings:

    def __init__(self):
        self.URL = None
        self.login = None
        self.password = None


class Settings:
    """
    Class that works with init.cfg file
    """
    def __init__(self):
        self.navi_port = ComPortSettings()
        self.depth_port = ComPortSettings()
        self.altimeter_port = ComPortSettings()
        self.inclin_port = ComPortSettings()
        self.temp_port = ComPortSettings()
        self.camera_settings = None
        self.default_folder = None
        self.config_file = 'resources/settings.xml'

    def ports_as_array(self):
        return (self.navi_port,
                self.depth_port,
                self.altimeter_port,
                self.inclin_port,
                self.temp_port)

    def readInitParamsDictionary(self):
        # By default it takes file "init.cfg" and makes a dictionary of it
        # init.cfg exapmple:
        output_parameters = {}
        try:
            with open(self.config_file, 'r') as ini_file:
                for line in ini_file:
                    line = line.rstrip().split('=')
                    for i in line:
                        try:
                            current_paramter_value = int(line[1])
                        except ValueError:
                            current_paramter_value = line[1].strip(" ")
                        output_parameters[line[0].strip(' ')] = current_paramter_value
            print("Initialized successful")
            return output_parameters
        except IOError:
            print("ERROR SonarInit: can not load " + ini_file)
            return 0


    def readSettings(self):
        # Read settings from XML file
        tree = ET.parse(self.config_file)
        root = tree.getroot()
        for chan in root.iter('channel'):
            # Read all
            for keyword, port_obj in zip(data_keywords.as_array, self.ports_as_array()):
                if chan.attrib['id'] == keyword:
                    port_obj.enable = int(chan[0].text)
                    port_obj.port = str(chan[1].text)
                    port_obj.rate = int(chan[2].text)
                    port_obj.message = str(chan[3].text)




def getInitParameters(ini_file = 'resources/init.cfg'):
    # By default it takes file "init.cfg" and makes a dictionary of it
    # init.cfg exapmple:

    output_parameters = {}
    try:
        with open(ini_file, 'r') as ini_file:
            for line in ini_file:
                line = line.rstrip().split('=')
                for i in line:
                    try:
                        current_paramter_value = int(line[1])
                    except ValueError:
                        current_paramter_value = line[1].strip(" ")
                    output_parameters[line[0].strip(' ')] = current_paramter_value
        print("Initialized successful")
        return output_parameters
    except IOError:
        print("ERROR SonarInit: can not load " + ini_file)
        return 0

def getCOMlist():
    pass





if __name__ == '__main__':
    
    # settings = Settings()
    # a = settings.readInitParamsDictionary()
    # print(a)
    # Test XML settings view

    tree = ET.parse('resources/settings.xml')
    root = tree.getroot()
    print(root.tag)

    for child in root:
        print(child.tag, child.attrib)
