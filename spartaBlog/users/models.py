# encoding: utf-8
from __future__ import unicode_literals

import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from spartaBlog import settings


def avatar_upload_to(instance, filename):
    return os.path.join(settings.MEDIA_ROOT, 'avatar', instance.user.username + os.path.splitext(filename)[1])


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    avatar = models.ImageField(upload_to=avatar_upload_to)


class FacebookProfile(models.Model):
    user = models.OneToOneField(User)
    facebook_id = models.BigIntegerField(null=True)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        FacebookProfile.objects.get_or_create(user=instance)


# сигнал, при создании нового пользователя автоматически создаестся facebook профиль
post_save.connect(create_user_profile, sender=User)
