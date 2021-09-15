import socket
import Course


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


# Working part of the script

keldyshSocket = createAndConnectSocket(KELDYSH_HOST, KELDYSH_PORT)
sonarSocket = createAndConnectSocket(SONAR_HOST, SONAR_PORT)

while True:
    keldyshGps = getGpgga(keldyshSocket.recv(1024))
    sonarGps = getGpgga(sonarSocket.recv(1024))
    
    if keldyshGps and sonarGps:
        print('K:', keldyshGps)
        print('S:', sonarGps)
        print(Course.calculate_course(keldyshGps, sonarGps))