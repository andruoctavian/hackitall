from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^signup$', views.signup_action, name='action.signup'),
    url(r'^login', views.login_action, name='action.login'),
    url(r'^logout', views.logout_action, name='action.logout'),
    url(r'^check', views.check_action, name='action.check'),
]
