from django.conf.urls import url, include
from . import views

urlpatterns = [
    # index
    url(r'^plates/$', views.plates.as_view()),
    url(r'^peers/$', views.peers.as_view()),
    url(r'^state/$', views.state.as_view()),
]
