import socket
import Course
from functools import reduce
import operator


# Defines

KELDYSH_HOST = '172.16.41.3'    # The Keldysh's GPS IP address
KELDYSH_PORT = 5017             # The Keldysh's GPS port

SONAR_HOST = '172.16.41.66'     # The Sonars's GPS IP address
SONAR_PORT = 5555               # The SOnars's GPS port


# Functions

def createAndConnectSocket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    return s

def getGpgga(data):
    nmeaString = data.decode('ascii')
    lines = nmeaString.split('\n')
    
    for line in lines:
        if line.startswith('$GPGGA'):
            gpGgaList = line.split(',')

            if len(gpGgaList) > 10:
                return [float(gpGgaList[2]), gpGgaList[3], float(gpGgaList[4]), gpGgaList[5]]

def createNmeaHeadingString(heading_value):
    """
    Creates $GPHDT line based on input date
    """
    hdt_string = 'GPHDT,{0:.1f},T'.format(heading_value)
    checksum = '*%02X' % reduce(operator.xor, map(ord, hdt_string), 0)
    hdt_string = '$' + hdt_string + str(checksum)
    send_message = hdt_string + '\r\n'

    return send_message


# Working part of the script

keldyshSocket = createAndConnectSocket(KELDYSH_HOST, KELDYSH_PORT)
sonarSocket = createAndConnectSocket(SONAR_HOST, SONAR_PORT)

hdt_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hdt_server.bind(('127.0.0.1', 5556))
hdt_server.listen()
conn, addr = hdt_server.accept()
print('Connected by ', addr)

while True:
    keldyshGps = getGpgga(keldyshSocket.recv(1024))
    sonarGps = getGpgga(sonarSocket.recv(1024))
    
    if keldyshGps and sonarGps:
        print('K:', keldyshGps)
        print('S:', sonarGps)
        heading = Course.calculate_course(sonarGps, keldyshGps)
        hdt = createNmeaHeadingString(heading)
        conn.sendall(bytes(hdt.encode('ascii')))
        print(heading)
        print(hdt)