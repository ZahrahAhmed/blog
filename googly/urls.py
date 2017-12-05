from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^place/search/$', views.pts, name="place-search"), 
    url(r'^place/detail/$', views.place_detail, name="place-detail"), 
    ]