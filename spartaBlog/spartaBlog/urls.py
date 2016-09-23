from django.conf.urls import include, url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blogApp.urls')),
    url(r'^registration$', views.RegisterFormView.as_view()),
    url(r'^login/', views.LoginFormView.as_view()),
    url(r'^logout$', views.LogoutView.as_view()),
    url(r'^password_reset/$', views.reset_user_password),
    url(r'^reset/done/$', views.reset_password_done),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.password_confirm, name='password_confirm'),
    url(r'^success/$', views.success, name='success'),
    url('^', include('django.contrib.auth.urls')),
    url('^$', views.index),
]
