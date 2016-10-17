# coding: utf-8
import os
import json
import urllib
import simplejson
import urlparse
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import password_reset, password_reset_confirm, password_reset_done
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from .forms import UserCreateForm, ProfileAvatarForm
from models import UserProfile, FacebookProfile
from spartaBlog import settings


class RegisterFormView(FormView):
    """Вьюха регистрации пользователя"""
    form_class = UserCreateForm

    success_url = "/login"
    template_name = "registration.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    """Вьюха логирования на сайт"""
    form_class = AuthenticationForm

    success_url = "/blog"
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()

        context = {'facebook_login_url': 'https://www.facebook.com/v2.8/dialog/oauth?client_id=%s&redirect_uri=%s' % (settings.FACEBOOK_APP_ID, settings.FACEBOOK_REDIRECT_URL),
                   'form': form
                   }
        return render(request, template_name="login.html", context=context)

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()

        # Выполняем аутентификацию пользователя.
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):

    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)

        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/login")


def reset_user_password(request):
    """Страница сброса пароля"""
    return password_reset(request=request, template_name='password_reset_form.html',
                          post_reset_redirect=reverse('success'))


def success(request):
    """Страница показывается после отсылки почты юзары, с сылкой на смену пароля"""
    return render(request, template_name='success.html')


def index(request):
    """Главная страница сайта"""
    return render(request, template_name='index.html')


def password_confirm(request, uidb64=None, token=None):
    """Страница ввода нового пароля"""
    return password_reset_confirm(request, template_name='password_reset_confirm.html', token=token, uidb64=uidb64)


def reset_password_done(request):
    """Страница успешной смены пароля"""
    return password_reset_done(request, template_name="password_reset_done.html")


class Profile(View):
    """Страница просмотра профиля пользователя"""

    @method_decorator(login_required)
    def get(self, request):
        avatar = ""
        if UserProfile.objects.filter(user_id=request.user.id):
            profile = UserProfile.objects.get(user_id=request.user.id)
            avatar = settings.MEDIA_URL + 'avatar/' + os.path.basename(profile.avatar.path)

        user_name = request.user.username

        load_avatar_form = ProfileAvatarForm()
        context = {"avatar_forms": load_avatar_form, "avatar": avatar, "user_name": user_name}

        return render(request, template_name='profile.html', context=context)

    def post(self, request):
        """Обрабатываем добавление аватарки"""
        load_avatar_form = ProfileAvatarForm(request.POST, request.FILES)
        if load_avatar_form.is_valid():
            if UserProfile.objects.filter(user_id=request.user.id):
                # удаляем старую запись
                profile = UserProfile.objects.get(user_id=request.user.id)
                os.remove(profile.avatar.path)
                profile.delete()

            # добавляем новую аватарку
            user_avatar = load_avatar_form.save(commit=False)
            user_avatar.user = request.user
            user_avatar.save()

        context = {"avatar_forms": load_avatar_form}

        return render(request, template_name='profile.html', context=context)


class FacebookLoginView(View):

    def get(self, request):
        access_token = self.get_access_token()
        facebook_data = self.get_facebook_data(access_token)
        try:
            profile = FacebookProfile.objects.get(facebook_id=facebook_data['id'])
        except FacebookProfile.DoesNotExist:
            user = self.create_user(facebook_data)
        else:
            user = profile.user

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        if user.is_active:
            login(request, user)
        # else:
        #     messages.error(request, 'Ваша учетная запись заблокирована!')
        return redirect('/blog/')

    def get_access_token(self):
        code = self.request.GET.get('code', '')
        graph_url = u"https://graph.facebook.com/v2.8/oauth/access_token?" + urllib.urlencode({
            'client_id': settings.FACEBOOK_APP_ID,
            'redirect_uri': settings.FACEBOOK_REDIRECT_URL,
            'client_secret': settings.FACEBOOK_SECRET,
            'code': code
        })

        response = urllib.urlopen(graph_url)
        content = response.read()
        data = json.loads(content)
        return data['access_token']

    def get_facebook_data(self, access_token):
        graph_url = "https://graph.facebook.com/v2.8/me?fields=email&" + urllib.urlencode({'access_token': access_token})
        response = urllib.urlopen(graph_url)
        content = response.read()
        data = simplejson.loads(content)
        return data

    def create_user(self, facebook_data):
        username = facebook_data['name']
        password = User.objects.make_random_password()

        user = User(
            username=username,
            email=facebook_data.get('email', None),
            is_staff=False,
            is_active=True,
            is_superuser=False,
        )
        user.set_password(password)
        user.save()

        return user


def facebook_privacy(request):
    """Главная страница сайта"""
    return render(request, template_name='facebook_privacy.html')
