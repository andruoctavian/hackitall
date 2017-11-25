# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from json import loads

from django.contrib.auth import models, authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError

from gogreen.services import *
from services import *

USERNAME_KEY = 'username'
EMAIL_KEY = 'email'
PASSWORD_KEY = 'password'
FIRST_NAME_KEY = 'first_name'
LAST_NAME_KEY = 'last_name'


@csrf_exempt
def signup_action(request):
    if is_authenticated(request):
        return fail_response('A user is already authenticated.')
    if not request_is_post(request):
        return fail_response('Expected POST request, received ' + request.method + '.')

    signup_form = loads(request.body)

    username = dict_get(signup_form, USERNAME_KEY)
    if username is None:
        return fail_response('No Username!')

    email = dict_get(signup_form, EMAIL_KEY)
    if email is None:
        return fail_response('No Email!')

    password = dict_get(signup_form, PASSWORD_KEY)
    if password is None:
        return fail_response('No Password!')

    first_name = dict_get(signup_form, FIRST_NAME_KEY)
    if first_name is None:
        return fail_response('No First Name!')

    last_name = dict_get(signup_form, LAST_NAME_KEY)
    if last_name is None:
        return fail_response('No Last Name!')

    try:
        user = models.User.objects.create_user(username=username, email=email, password=password)
    except IntegrityError:
        return fail_response('There is already a user with the same username signed up.')

    user.first_name = first_name
    user.last_name = last_name

    try:
        user.save()
    except Exception:
        return fail_response('Unexpected error while creating new user.')

    return success_response('User Created')


@csrf_exempt
def login_action(request):
    if is_authenticated(request):
        return fail_response('A user is already authenticated.')
    if not request_is_post(request):
        return fail_response('Expected POST request, received ' + request.method + '.')

    login_form = loads(request.body)

    username = dict_get(login_form, USERNAME_KEY)
    if username is None:
        return fail_response('No Username!')

    password = dict_get(login_form, PASSWORD_KEY)
    if password is None:
        return fail_response('No Password!')

    user = authenticate(username=username, password=password)
    if user is None:
        return fail_response('Wrong credentials!')

    login(request, user)
    return success_response(request.session.session_key)


@csrf_exempt
def logout_action(request):
    if not is_authenticated(request):
        return fail_response('There is no user authenticated.')
    try:
        logout(request)
    except Exception:
        return fail_response('Unexpected error while logging out.')

    return success_response('User logged out.')


@csrf_exempt
def check_action(request):
    if not is_authenticated(request):
        return fail_response('There is no user authenticated.')

    return success_response('User is Logged in.')
