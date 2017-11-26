# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, JsonResponse
from json import loads
from requests import get
from gogreen import settings

# Create your views here.


@csrf_exempt
def index(request):
    origin = request.GET.get('origin', '')
    destination = request.GET.get('destination', '')
    api_response = get(settings.GOOGLE_API_DIRECTION_URL, params={
        'key': settings.GOOGLE_API_KEY,
        'origin': 'Bucharest',
        'destination': 'Focsani',
    })

    json_response = JsonResponse(loads(api_response.content))

    return json_response
