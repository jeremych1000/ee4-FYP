from django.conf.urls import url, include
from . import views
from .cron import *

urlpatterns = [
    # index
    url(r'^register/$', views.register.as_view(), name='register'),

    url(r'^update/$', views.update.as_view(), name='update'),

    url(r'^keep_alive/$', views.keep_alive.as_view(), name='keep_alive'),

    # cron stuff
    url(r'^get_peer_list/$', views.get_peers.as_view(), name='get_peers'),
]
