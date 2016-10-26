# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-21 02:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workouts', '0018_auto_20161014_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='routine',
            name='modified_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='routine',
            name='modify_date',
            field=models.DateTimeField(null=True, verbose_name='date modified'),
        ),
        migrations.AlterField(
            model_name='routine',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='routine',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published'),
        ),
    ]