# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt

from gogreen.services import *
from AuthApp.services import is_authenticated
from .services import *
from .breezometer_service import breezometer_route

ORIGIN_KEY = 'origin'
DESTINATION_KEY = 'destination'
MODE_KEY = 'mode'
MODE_DRIVING = 'driving'


@csrf_exempt
def directions(request, green_index):
    if not is_authenticated(request):
        return fail_response('User is not authenticated.')

    origin = adapt_invert(request.GET.get(ORIGIN_KEY, None))
    if origin is None:
        return fail_response('No origin')

    destination = adapt_invert(request.GET.get(DESTINATION_KEY, None))
    if destination is None:
        return fail_response('No destination')

    mode = request.GET.get(MODE_KEY, MODE_DRIVING)

    if int(green_index) == 0:
        return JsonResponse([], safe=False)

    google_response = call_google(origin, destination, mode)
    if not check_google_response(google_response):
        return fail_response('No routes were found.')

    way_points = breezometer_route(google_response,int(green_index))
    way_points = adapt_google(way_points)

    return JsonResponse(way_points, safe=False)
