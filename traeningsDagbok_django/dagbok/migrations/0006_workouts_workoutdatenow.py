# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-18 08:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dagbok', '0005_auto_20160518_0829'),
    ]

    operations = [
        migrations.AddField(
            model_name='workouts',
            name='workoutDateNow',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 5, 18, 8, 33, 12, 754278, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
