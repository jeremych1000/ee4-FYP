from django.conf.urls import url, include
from . import views

urlpatterns = [
    # index
    url(r'^plates/$', views.plates.as_view()),


    url(r'status/$', views.status.as_view()),
]
