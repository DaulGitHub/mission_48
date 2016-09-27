from __future__ import unicode_literals

import os
from django.db import models
from django.contrib.auth.models import User


def avatar_upload_to(instance, filename):
    return os.path.join('uploads', instance.user.username + os.path.splitext(filename)[1])


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    avatar = models.ImageField(upload_to=avatar_upload_to)
