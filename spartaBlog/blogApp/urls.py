from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.comments, name='comments'),
    url(r'^wall/(?P<wall_owner>.*)$', views.wall),
    url(r'^messages/(?P<companion>.*)$', views.chat),
    url(r'^instagram_photos/$', views.instagram_photos),
]