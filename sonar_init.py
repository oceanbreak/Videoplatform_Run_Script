""" Module that works with init.cfg files for sonar programs"""

import sys

def Get_Init_Parameters(ini_file = 'resources/init.cfg'):
    # By default it takes file "init.cfg" and makes a dictionary of it
    # init.cfg exapmple:
    #
    #COM_PORT = COM7
    #SPEED = 9600
    #PREIOD = 5
    #LENGTH = 1500
    #
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

if __name__ == '__main__':
    try:
        print(Get_Init_Parameters())#(sys.argv[1])
    except IndexError:
        print("Usage: sonar_init.py <init.cfg>")


