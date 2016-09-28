from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
import settings


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blogApp.urls')),
    url(r'^', include('users.urls')),
    url('^', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

