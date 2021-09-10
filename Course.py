from math import *


def calculate_course(coords_lab, coords_bridge):
    """ Get coordinates from the ship's bridge and from Sonar Lab's
    gps-receiver and calculate the ship's true (not-magnetic) course
    over ground (COV), considering loxodrome.
    :param: Coordinates = list: coords_bridge = [latitude, 'N', longitude, 'N']
    Latitude = float: DDMM.MMMMMM, 'N'
    Longitude = float: DDDMM.MMMMMM, 'E'
    :return: course: float in degrees
    Formula from https://www.movable-type.co.uk/scripts/latlong.html
    Works in all hemispheres, but only when lab and bridge are in the
    same hemisphere.
    """
    coords_lab = parse_input_coords(coords_lab)
    coords_bridge = parse_input_coords(coords_bridge)
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
    course = atan2(delta_lambda, delta_psi) * 180 / pi
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
    TODO: work only in N E hemisphere
    """
    DISTANCE_FROM_LAB_TO_VM = 30  # meters
    CORRECTION_ANGLE = 0  # degrees
    R = 6371000
    course = radians(360 - course + CORRECTION_ANGLE)
    coords_lab = parse_input_coords(coords_lab)
    lat_lab = radians(coords_lab[0])
    lon_lab = radians(coords_lab[2])
    lat_vm = lat_lab - DISTANCE_FROM_LAB_TO_VM / R * cos(course)
    delta_fi = lat_vm - lat_lab
    delta_psi = log(tan(pi/4 + lat_vm/2) / tan(pi/4 + lat_lab/2))
    if delta_psi > 10e-12:
        q = delta_fi/delta_psi
    else:
        q = cos(lat_lab)
    lon_vm = lon_lab + DISTANCE_FROM_LAB_TO_VM/R*sin(course)/q
    if abs(lat_vm) > pi/2:
        if lat_vm > 0:
            lat_vm = pi - lat_vm
        else:
            lat_vm = -pi - lat_vm
    return [degrees(lat_vm), coords_lab[1], degrees(lon_vm), coords_lab[3]]


def parse_input_coords(input_coords: [float, str, float, str]):
    """
    :param input_coords: from gps, format DDMM.MMMMMM, 'N'
    :return: coords in format DD.DDDDDD, 'N'
    where D is degree
    """
    latitude = input_coords[0]
    longitude = input_coords[2]
    lat_degrees = latitude//100
    lon_degrees = longitude//100
    lat_minutes = latitude % 100
    lon_minutes = longitude % 100
    return [lat_degrees + lat_minutes/60, input_coords[1],
            lon_degrees + lon_minutes/60, input_coords[3]]


if __name__ == '__main__':
    print("Course is:",
          calculate_course([7300.00000, 'S', 05700.0000, 'E'],
                           [7400.000000, 'S', 05800.00000, 'E']), 'degrees')
    print(calculate_vm_coords([7300.00000, 'N', 05700.0000, 'W'], 310))
