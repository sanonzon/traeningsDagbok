# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-18 08:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dagbok', '0003_workouts_workoutsport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workouts',
            name='workoutDate',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]