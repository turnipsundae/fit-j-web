# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-02 04:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0020_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='Completed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(max_length=1000)),
                ('completed_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('journal_entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workouts.Journal')),
            ],
        ),
    ]
