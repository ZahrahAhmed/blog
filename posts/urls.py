from django.conf.urls import url
from posts import views

urlpatterns = [
    url(r'^home/$', views.home, name="home"),
     url(r'^home1/$', views.home1, name="home1"),
     url(r'^home2/$', views.home2, name="home2"),
     url(r'^list/$', views.post_list, name="list"),
     url(r'^detail/(?P<post_id>\d+)/$', views.post_detail, name="detail"),
]
