"""This module takes n_v files, reads coordinates in format DDMM.MMMMMM Lat, DDDMM.MMMMMM Lon,
transforms it into format DD.DDDDDD (Lat/Lon) and generates comma separated .dat file for surfer
Also calculates distance between coordinates"""


from math import radians, cos, sin, asin, sqrt

#Gives output data proper sign
coord_sign = {'N':1, 'S':-1, 'E':1, 'W':-1}


def haversine(coord_a, coord_b):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [coord_a[1], coord_a[0], coord_b[1], coord_b[0]])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r * 1000 # in meters



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

def convertCoordtoDeg(degr_lat, min_lat, lat, degr_lon, min_lon, lon):
    """
    Converts an array of values DD, MM.MMM, (S,N,E,W)
    :return: coordinates in format [DD.DDDD, DD.DDDD]
    """
    degr_lat = int(degr_lat)
    min_lat = float(min_lat)
    degr_lon = int(degr_lon)
    min_lon  =float(min_lon)
    return [coord_sign[lat] * (degr_lat + min_lat / 60), coord_sign[lon] * (degr_lon + min_lon / 60)]

def convertCoordtoDM(lat, lon):
    letter_lat = 'N' if lat > 0.0 else 'S'
    letter_lon = 'E' if lon > 0.0 else 'W'

    lat = abs(lat)
    lon = abs(lon)

    degr_lat = lat // 1
    min_lat = lat % 1 * 60

    degr_lon = lon // 1
    min_lon = lon % 1 * 60

    return (degr_lat, min_lat, letter_lat, degr_lon, min_lon, letter_lon)
    

def calculateTrack(coord1, coord2, units='m'):
    if units == 'm':
        return haversine(coord1, coord2)
    elif units == 'miles':
        return haversine(coord1, coord2)/1800


if __name__ == '__main__':
    c_a = convertCoordtoDeg("78 09.1843'N, 116 37.6358'E")
    c_b = convertCoordtoDeg("78 06.1843'N, 115 37.6358'E")
    print(c_a, c_b)
    print(calculateTrack(c_a, c_b))