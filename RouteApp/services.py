
from math import sin, cos, sqrt, atan2, radians

from .api_service import RADIUS, LATITUDE_KEY

# approximate radius of earth in km
R = 6373.0
LOCATION_KEY = 'location'
LONGITUDE_KEY = 'lng'
STOPOVER_KEY = 'stopover'
RESULTS_KEY = 'results'
GEOMETRY_KEY = 'geometry'
DISTANCE_KEY = 'distance'


def adapt_google(way_points):
    google_formatted = []
    for way_point in way_points:
        google_formatted.append({
            LOCATION_KEY: str(way_point[0]) + ',' + str(way_point[1]),
            STOPOVER_KEY: True
        })

    return google_formatted


def adapt_invert(coordinates):
    if coordinates is None:
        return None

    coord1, coord2 = coordinates.split(",")

    return coord2 + "," + coord1


def get_lat_lon_distance(lat1, lon1, lat2, lon2):
    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def get_closest_place(latitude, longitude, google_response):
    results = google_response[RESULTS_KEY]
    if len(results) == 0:
        return None

    x_latitude = None
    x_longitude = None
    x_distance = RADIUS
    for place in results:
        d = get_lat_lon_distance(
            latitude, longitude,
            place[GEOMETRY_KEY][LOCATION_KEY][LATITUDE_KEY], place[GEOMETRY_KEY][LOCATION_KEY][LONGITUDE_KEY]
        )
        if d < x_distance:
            x_latitude = place[GEOMETRY_KEY][LOCATION_KEY][LATITUDE_KEY]
            x_longitude = place[GEOMETRY_KEY][LOCATION_KEY][LONGITUDE_KEY]
            x_distance = d

    return {
        LATITUDE_KEY: x_latitude,
        LONGITUDE_KEY: x_longitude,
        DISTANCE_KEY: str(x_distance/1000) + " km"
    }
