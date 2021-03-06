# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-14 03:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workouts', '0012_auto_20161012_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='routine',
            name='created_by',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='routine',
            name='routine_text',
            field=models.TextField(),
        ),
    ]
