# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-07 10:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0003_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('user_from_id', models.IntegerField()),
                ('user_to_id', models.IntegerField()),
            ],
        ),
    ]
