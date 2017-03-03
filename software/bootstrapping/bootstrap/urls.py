from django.conf.urls import url, include
from . import views

urlpatterns = [
    # index
    url(r'^register/$', views.register.as_view(), name='register'),
    url(r'^get_peers/$', views.get_peers.as_view(), name='get_peers'),
]