# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-25 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20170121_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='is_seen',
            field=models.BooleanField(default=False, verbose_name='Is Message Seen'),
        ),
    ]
