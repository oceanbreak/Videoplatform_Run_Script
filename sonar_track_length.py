"""This module takes n_v files, reads coordinates in format DDMM.MMMMMM Lat, DDDMM.MMMMMM Lon,
transforms it into format DD.DDDDDD (Lat/Lon) and generates comma separated .dat file for surfer
Also calculates distance between coordinates"""

import sys, os
from haversine_custom import haversine

#Gives output data proper sign
coord_sign = {'N':1, 'S':-1, 'E':1, 'W':-1}

def convertCoordString(coord_string):
    """
    Input: coordinates in format DD MM.MMMM'N, DDD MM.MMMM'E
    :return: coordinates in format [DD.DDDD, DD.DDDD]
    """
    try:
        lat, lon = coord_string.split(',')
        lat, lon = lat.strip(), lon.strip()
    except IndexError:
        return [None, None]
    degr_lat, min_lat, sign_lat = int(lat[:2]), float(lat[3:10]), int(coord_sign[lat[11]])
    degr_lon, min_lon, sign_lon = int(lon[0:3]), float(lon[4:11]), int(coord_sign[lon[12]])
    return [sign_lat * (degr_lat + min_lat / 60), sign_lon * (degr_lon + min_lon / 60)]

def convertCoord(degr_lat, min_lat, lat, degr_lon, min_lon, lon):
    """
    Converts an array of values DD, MM.MMM, (S,N,E,W)
    :return: coordinates in format [DD.DDDD, DD.DDDD]
    """
    return [coord_sign[lat] * (degr_lat + min_lat / 60), coord_sign[lon] * (degr_lon + min_lon / 60)]

def calculateTrack(coord1, coord2, units='m'):
    if units == 'm':
        return haversine(coord1, coord2)
    elif units == 'mm':
        return haversine(coord1, coord2)/1800

if __name__ == '__main__':
    c_a = convertCoord("78 09.1843'N, 116 37.6358'E")
    c_b = convertCoord("78 06.1843'N, 115 37.6358'E")
    print(c_a, c_b)
    print(calculateTrack(c_a, c_b))