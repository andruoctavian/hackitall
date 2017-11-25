from django.http import JsonResponse

ERROR_KEY = 'error'
MESSAGE_KEY = 'message'


def success_response(message):
    return JsonResponse({
        ERROR_KEY: False,
        MESSAGE_KEY: message
    })


def fail_response(message):
    return JsonResponse({
        ERROR_KEY: True,
        MESSAGE_KEY: message
    })