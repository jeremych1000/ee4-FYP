from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^about/$', views.about, name='about'),
    url(r'^download/$', views.download, name='download'),
    url(r'^privacy/$', views.privacy, name='privacy'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^peers/$', views.peers, name='peers'),
    url(r'^violations/$', views.violations, name='violations'),
    url(r'^alpr(?P<dir>.+)$', views.get_alpr_image, name='alpr'),
    url(r'^blank/$', views.blank),
]
