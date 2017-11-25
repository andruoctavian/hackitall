# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

LOCATION_KEY = 'location'
STEP_OVER_KEY = 'stepover'


@csrf_exempt
def directions(request, green_index):
    origin = request.GET.get('origin', '')
    destination = request.GET.get('destination', '')

    way_points = [
        {LOCATION_KEY: 'Arcul de Triumf', STEP_OVER_KEY: True},
    ]

    return JsonResponse(way_points, safe=False)
