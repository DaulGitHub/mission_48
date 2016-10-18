from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login/', views.LoginFormView.as_view()),
    url(r'^logout/', views.LogoutView.as_view()),
    url(r'^password_reset/$', views.reset_user_password),
    url(r'^reset/done/$', views.reset_password_done),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.password_confirm,
        name='password_confirm'),
    url(r'^success/$', views.success, name='success'),
    url('^$', views.index),
    url(r'^profile/$', views.Profile.as_view()),
    url(r'^registration/$', views.RegisterFormView.as_view()),
    url(r'^facebook_login/$', views.FacebookLoginView.as_view()),
]