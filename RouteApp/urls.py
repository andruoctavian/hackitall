from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^directions/(?P<green_index>[0-9]+)$', views.directions, name='directions'),
]
