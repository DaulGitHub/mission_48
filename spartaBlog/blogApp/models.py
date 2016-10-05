# coding: utf8
import os
import random
import string
from django.contrib.auth.models import User
from django.db import models
from spartaBlog import settings

# Модифицируем поле email.
# _meta это экземпляр django.db.models.options.Options, который хранит данные о модели.
# Это немного хак, но я пока не нашел более простого способа переопределить поле из базовой модели.
User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False


class Comment(models.Model):
    user_name = models.CharField(max_length=30)
    message = models.TextField()


def post_upload_to(instance, filename):
    file_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
    return os.path.join('posts', file_name + os.path.splitext(filename)[1])


class Post(models.Model):
    commentator_name = models.CharField(max_length=30)
    message = models.TextField()
    wall_owner = models.CharField(max_length=30)
    photo = models.ImageField(upload_to=post_upload_to)
