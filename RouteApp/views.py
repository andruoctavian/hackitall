# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt

from gogreen.services import *
from AuthApp.services import is_authenticated
from .services import *
from .api_service import *
from .breezometer_service import breezometer_route, get_local_air_quality

ORIGIN_KEY = 'origin'
DESTINATION_KEY = 'destination'
MODE_KEY = 'mode'
MODE_DRIVING = 'driving'
PARK_KEY = 'park'


@csrf_exempt
def directions_action(request, green_index):
    if not is_authenticated(request):
        return fail_response('User is not authenticated.')

    origin = adapt_invert(request.GET.get(ORIGIN_KEY, None))
    if origin is None:
        return fail_response('No origin')

    destination = adapt_invert(request.GET.get(DESTINATION_KEY, None))
    if destination is None:
        return fail_response('No destination')

    mode = request.GET.get(MODE_KEY, MODE_DRIVING)

    park = request.GET.get(PARK_KEY, None)
    if park is not None:
        coordinates = origin.split(",")
        google_response = call_google_place(coordinates[0], coordinates[1], 'park')
        park = get_closest_place(coordinates[0], coordinates[1], google_response)
        park = [{
            LOCATION_KEY: str(park[LATITUDE_KEY]) + ',' + str(park['lng']),
            STOPOVER_KEY: True,
        }]
    else:
        park = []

    if int(green_index) == 0:
        return JsonResponse(park, safe=False)

    google_response = call_google_direction(origin, destination, mode)
    if not check_google_response(google_response):
        return fail_response('No routes were found.')

    way_points = breezometer_route(google_response, int(green_index))
    way_points = park + adapt_google(way_points)

    return JsonResponse(way_points, safe=False)


@csrf_exempt
def location_action(request):
    if not is_authenticated(request):
        return fail_response('User is not authenticated.')

    latitude = request.GET.get(LATITUDE_KEY, None)
    if latitude is None:
        return fail_response('No latitude specified.')

    longitude = request.GET.get(LONGITUDE_KEY, None)
    if longitude is None:
        return fail_response('No longitude specified.')

    return success_response(get_local_air_quality(latitude, longitude))


@csrf_exempt
def parks_action(request):
    if not is_authenticated(request):
        return fail_response('User is not authenticated.')

    latitude = request.GET.get(LATITUDE_KEY, None)
    if latitude is None:
        return fail_response('No latitude specified.')

    longitude = request.GET.get(LONGITUDE_KEY, None)
    if longitude is None:
        return fail_response('No longitude specified.')

    google_response = call_google_place(latitude, longitude, 'park')
    location = get_closest_place(latitude, longitude, google_response)

    if location is None:
        return fail_response("There is no park in the area.")

    return success_response(location)

