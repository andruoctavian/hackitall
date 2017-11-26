from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^directions/(?P<green_index>[0-9]+)$', views.directions_action, name='action.directions'),
    url(r'^location$', views.location_action, name='action.location'),
    url(r'^parks$', views.parks_action, name='action.park'),
]
