from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.comments, name='comments'),
    url(r'^wall/(?P<wall_owner>.*)$', views.wall),
]