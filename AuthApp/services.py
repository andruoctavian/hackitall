
from django.http import HttpRequest
from django.contrib.sessions.models import Session
from django.utils import timezone


TOKEN_KEY = 'token'


def request_is_post(request):
    if not isinstance(request, HttpRequest):
        return False

    return request.method == 'POST'


def dict_get(collection, key):
    return collection[key] if key in collection else None


def is_authenticated(request):
    if not isinstance(request, HttpRequest):
        return False

    if request_is_post(request):
        session_key = request.POST.get(TOKEN_KEY, None)
    else:
        session_key = request.GET.get(TOKEN_KEY, None)
    if session_key is None:
        return False

    session = Session.objects.filter(expire_date__gte=timezone.now()).filter(session_key=session_key)

    return session.exists()
