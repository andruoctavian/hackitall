
from django.http import HttpRequest
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils import timezone


TOKEN_KEY = 'token'
AUTH_USER_ID_KEY = '_auth_user_id'


def request_is_post(request):
    if not isinstance(request, HttpRequest):
        return False

    return request.method == 'POST'


def dict_get(collection, key):
    return collection[key] if key in collection else None


def is_authenticated(request):
    if not isinstance(request, HttpRequest):
        return False

    session_key = request.GET.get(TOKEN_KEY, None)
    if session_key is None:
        return False

    session = Session.objects.filter(expire_date__gte=timezone.now()).filter(session_key=session_key)

    return session.exists()


def get_user(request):
    if not isinstance(request, HttpRequest):
        return None

    session_key = request.GET.get(TOKEN_KEY, None)
    if session_key is None:
        return None

    session = Session.objects.filter(expire_date__gte=timezone.now()).filter(session_key=session_key)
    if not session.exists():
        return None

    uid = session.first().get_decoded().get(AUTH_USER_ID_KEY, None)
    if uid is None:
        return None

    user = User.objects.get(pk=uid)
    if user is None:
        return None

    return user


def serialize_user(user):
    if not isinstance(user, User):
        return {}

    return {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
