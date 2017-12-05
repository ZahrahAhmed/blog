from django.conf.urls import url
from . import views 

urlpatterns = [
    url(r'^twitt/$', views.twitt, name="members"),
]
