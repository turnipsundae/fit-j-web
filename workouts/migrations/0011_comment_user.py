# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-25 17:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0010_auto_20160925_1004'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='workouts.User'),
            preserve_default=False,
        ),
    ]
