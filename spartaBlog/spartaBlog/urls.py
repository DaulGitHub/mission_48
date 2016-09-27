from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blogApp.urls')),
    url(r'^', include('users.urls')),
    url('^', include('django.contrib.auth.urls')),
]

