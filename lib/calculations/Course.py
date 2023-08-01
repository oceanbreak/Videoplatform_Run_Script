from math import *


def calculate_course(coords_lab, coords_bridge):
    """ Get coordinates from the ship's bridge and from Sonar Lab's
    gps-receiver and calculate the ship's true (not-magnetic) course
    over ground (COV), considering loxodrome.
    :param: Coordinates = list: coords_bridge = [latitude, 'N',
     longitude, 'N']
    Latitude = float: DDMM.MMMMMM, 'N'
    Longitude = float: DDDMM.MMMMMM, 'E'
    :return: course: float in degrees
    Formula from https://www.movable-type.co.uk/scripts/latlong.html
    Works in all hemispheres, but only when lab and bridge are in the
    same hemisphere.
    """
    CORRECTION_ANGLE = 17  # degrees
    coords_lab = parse_coords_from_ddmm_to_dd(coords_lab)
    coords_bridge = parse_coords_from_ddmm_to_dd(coords_bridge)
    lat_bridge = radians(coords_bridge[0])
    lon_bridge = radians(coords_bridge[2])
    # lat_hemisphere_bridge = coords_bridge[1]
    # lon_hemisphere_bridge = coords_bridge[3]
    lat_lab = radians(coords_lab[0])
    lon_lab = radians(coords_lab[2])
    lat_hemisphere_lab = coords_lab[1]
    lon_hemisphere_lab = coords_lab[3]
    delta_psi = log(tan(pi/4 + lat_bridge/2) / tan(pi/4 + lat_lab/2))
    if lat_hemisphere_lab == 'S':
        delta_psi = -delta_psi
    delta_lambda = lon_bridge - lon_lab
    if abs(delta_lambda) > pi:
        if delta_lambda > 0:
            delta_lambda = -(2*pi - delta_lambda)
        else:
            delta_lambda = 2*pi + delta_lambda
    course = atan2(delta_lambda, delta_psi) * 180 / pi - CORRECTION_ANGLE
    if course < 0:
        course = 360 + course
    return course if lon_hemisphere_lab == 'E' else 360 - course


def calculate_vm_coords(coords_lab: [float, str, float, str], course):
    """
    Calculate coordinates of the Videomodule(TM) using coordinates of the
    lab and the course of the Keldysh. Course is inverted because Videomodule
    is backward from the lab.
    Formula from https://www.movable-type.co.uk/scripts/latlong.html
    :param coords_lab: format DDMM.MMMMMM, 'N', DDDMM.MMMMMM, 'N'
    :param course: degrees
    :return: coordinates of the Videomodule in format DD.DDDDDD, 'N',
    DDD.DDDDDDD, 'N'
    """
    DISTANCE_FROM_LAB_TO_VM = 21.89  # meters
    CORRECTION_ANGLE = 7  # degrees
    R = 6371000
    course = radians((course + 180) % 360 - CORRECTION_ANGLE)
    coords_lab = parse_coords_from_ddmm_to_dd(coords_lab)
    lat_lab = radians(coords_lab[0])
    lon_lab = radians(coords_lab[2])
    lat_hemisphere_lab = coords_lab[1]
    lon_hemisphere_lab = coords_lab[3]
    delta_fi = DISTANCE_FROM_LAB_TO_VM / R * cos(course)
    if lat_hemisphere_lab == "S":
        delta_fi = -delta_fi
    lat_vm = lat_lab + delta_fi
    delta_psi = log(tan(pi/4 + lat_vm/2) / tan(pi/4 + lat_lab/2))
    if abs(delta_psi) > 10e-12:
        q = delta_fi/delta_psi
    else:
        q = cos(lat_lab)
    delta_lambda = DISTANCE_FROM_LAB_TO_VM / R * sin(course) / q
    if lat_hemisphere_lab == "S" and lon_hemisphere_lab == "W":
        delta_lambda = -delta_lambda
    if lat_hemisphere_lab == "N" and lon_hemisphere_lab == "W":
        delta_lambda = -delta_lambda
    lon_vm = lon_lab + delta_lambda
    if abs(lat_vm) > pi/2:
        if lat_vm > 0:
            lat_vm = pi - lat_vm
        else:
            lat_vm = -pi - lat_vm
    return parse_coords_from_dd_to_ddmm(
        [degrees(lat_vm), coords_lab[1], degrees(lon_vm), coords_lab[3]])


def parse_coords_from_ddmm_to_dd(input_coords: [float, str, float, str]):
    """
    :param input_coords: from gps, format DDMM.MMMMMM, 'N'
    :return: coords in format DD.DDDDDD, 'N'
    where D is degree, M is minute.
    """
    latitude = input_coords[0]
    longitude = input_coords[2]
    lat_degrees = latitude//100
    lon_degrees = longitude//100
    lat_minutes = latitude % 100
    lon_minutes = longitude % 100
    return [lat_degrees + lat_minutes/60, input_coords[1],
            lon_degrees + lon_minutes/60, input_coords[3]]


def parse_coords_from_dd_to_ddmm(input_coords: [float, str, float, str]):
    """
        :param input_coords: 'my' format DD.DDDDDD, 'N'
        :return: coords in gps format DDMM.MMMMMM, 'N'
        where D is degree, M is minute.
        """
    latitude = input_coords[0]
    longitude = input_coords[2]

    return [latitude//1 * 100 + latitude % 1 * 60, input_coords[1],
            longitude//1 * 100 + longitude % 1 * 60, input_coords[3]]





if __name__ == '__main__':
    print("Course is:",
          calculate_course([7300.00000, 'N', 05700.0000, 'E'],
                           [7200.000000, 'N', 05600.00000, 'E']), 'degrees')
    print("Course is:",
          calculate_course([7447.2025348, 'N', 6803.1005464, 'E'],
                           [7447.19116954, 'N', 6803.01404081, 'E']), 'degrees')
    # print(calculate_vm_coords([7300.00000, 'S', 05700.0000, 'W'], 45))
    # print(parse_coords_from_dd_to_ddmm([73.5000000, 'S', 057.500000, 'E'],))
"""
k: [7447.19116954, 'N', 6803.01404081, 'E']
S: [7447.2025348, 'N', 6803.1005464, 'E']
"""