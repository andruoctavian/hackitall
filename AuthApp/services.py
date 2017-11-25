
from django.http import HttpRequest


def request_is_post(request):
    if not isinstance(request, HttpRequest):
        return False

    return request.method == 'POST'


def dict_get(collection, key):
    return collection[key] if key in collection else None
