# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-15 00:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0015_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal',
            name='completed_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='journal',
            name='completed_on',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 15, 0, 54, 20, 726987, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
