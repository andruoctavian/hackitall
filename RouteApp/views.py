# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

LOCATION_KEY = 'location'
STOPOVER_KEY = 'stopover'


@csrf_exempt
def directions(request, green_index):
    origin = request.GET.get('origin', '')
    destination = request.GET.get('destination', '')

    way_points = [
        {LOCATION_KEY: 'Arcul de Triumf', STOPOVER_KEY: True},
    ]

    return JsonResponse(way_points, safe=False)
