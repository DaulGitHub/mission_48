from django.conf.urls import include, url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('blogApp.urls')),
    url(r'^registration$', views.RegisterFormView.as_view()),
    url(r'^login/', views.LoginFormView.as_view()),
    url(r'^logout$', views.LogoutView.as_view()),
    # url(r'^resetpassword/$', 'django.contrib.auth.views.password_reset'),
    # url(r'^resetpassword/$', views.reset_user_password),
    # url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^success/$', views.success, name='success'),
    url('^', include('django.contrib.auth.urls')),
    url('^$', views.index),
]
