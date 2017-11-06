from django.conf.urls import url
from posts import views

urlpatterns = [
    url(r'^home/$', views.post_home, name="home"), 
    url(r'^home2/$', views.post_home2, name="home2"), 
]