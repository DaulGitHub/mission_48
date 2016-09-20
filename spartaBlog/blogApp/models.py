# coding: utf8
from django.contrib.auth.models import User

# Модифицируем поле email.
# _meta это экземпляр django.db.models.options.Options, который хранит данные о модели.
# Это немного хак, но я пока не нашел более простого способа переопределить поле из базовой модели.
User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
