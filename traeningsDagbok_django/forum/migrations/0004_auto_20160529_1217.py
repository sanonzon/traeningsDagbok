# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-29 10:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.CharField(default='', max_length=255),
        ),
    ]
