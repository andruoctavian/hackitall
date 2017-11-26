
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


def call_google(origin, destination, mode):
    api_response = get(GOOGLE_API_URL, params={
        KEY: GOOGLE_API_KEY,
        ORIGIN_KEY: origin,
        DESTINATION_KEY: destination,
        MODE_KEY: mode,
    })

    return loads(api_response.content)


def call_breezometer(latitude, longitude):
    return get(BREEZOMETER_API_URL, params={
        KEY: BREEZOMETER_API_KEY,
        LATITUDE_KEY: latitude,
        LONGITUDE_KEY: longitude,
        FIELDS_KEY: 'breezometer_aqi'
    })


def check_google_response(google_response):
    if len(google_response[ROUTES_KEY]) == 0:
        return False

    return True
