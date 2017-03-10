from django.conf.urls import url, include
from . import views

urlpatterns = [
    # index
    url(r'^get_plates/$', views.get_plates.as_view()),

]
