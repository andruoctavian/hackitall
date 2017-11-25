# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from json import loads
from django.views.decorators.csrf import csrf_exempt
from requests import get

from gogreen.services import *
from gogreen.settings import *
from AuthApp.services import is_authenticated
from .services import *
from.breezometer_service import breezometer_route


@csrf_exempt
def directions(request, green_index):
    if not is_authenticated(request):
        return fail_response('User is not authenticated.')

    origin = request.GET.get('origin', None)
    if origin is None:
        return fail_response('No origin')

    destination = request.GET.get('destination', None)
    if destination is None:
        return fail_response('No destination')

    api_response = get(GOOGLE_API_URL, params={
        'key': GOOGLE_API_KEY,
        'origin': origin,
        'destination': destination,
    })

    google_response = loads(api_response.content)
    if not check_google_response(google_response):
        return fail_response('No routes were found.')

    way_points = breezometer_route(google_response)
    way_points = adapt_google(way_points)

    return JsonResponse(way_points, safe=False)
