
from json import loads
from requests import get

from gogreen.settings import *

KEY = 'key'
ORIGIN_KEY = 'origin'
DESTINATION_KEY = 'destination'
MODE_KEY = 'mode'
ROUTES_KEY = 'routes'
LATITUDE_KEY = 'lat'
LONGITUDE_KEY = 'lon'
FIELDS_KEY = 'fields'
LOCATION_KEY = 'location'
TYPES_KEY = 'types'
RADIUS_KEY = 'radius'
RADIUS = 5000


def call_google_direction(origin, destination, mode):
    api_response = get(GOOGLE_API_DIRECTION_URL, params={
        KEY: GOOGLE_API_KEY,
        ORIGIN_KEY: origin,
        DESTINATION_KEY: destination,
        MODE_KEY: mode,
    })

    return loads(api_response.content)


def call_google_place(latitude, longitude, place_type):
    api_response = get(GOOGLE_API_PLACE_URL, params={
        KEY: GOOGLE_API_KEY,
        LOCATION_KEY: str(latitude) + "," + str(longitude),
        TYPES_KEY: place_type,
        RADIUS_KEY: RADIUS
    })

    return loads(api_response.content)


def call_breezometer(latitude, longitude, fields):
    return get(BREEZOMETER_API_URL, params={
        KEY: BREEZOMETER_API_KEY,
        LATITUDE_KEY: latitude,
        LONGITUDE_KEY: longitude,
        FIELDS_KEY: fields
    })


def check_google_response(google_response):
    if len(google_response[ROUTES_KEY]) == 0:
        return False

    return True
