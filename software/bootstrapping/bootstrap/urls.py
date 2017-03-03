from django.conf.urls import url, include
from . import views

urlpatterns = [
    # index
    url(r'^register/$', views.register.as_view(), name='register'),
    url(r'^deregister/$', views.deregister.as_view(), name='deregister'),

    url(r'^update/$', views.update.as_view(), name='update'),

    url(r'^keep_alive/$', views.keep_alive.as_view(), name='keep_alive'),

    url(r'^get_peers/$', views.get_peers.as_view(), name='get_peers'),
]
