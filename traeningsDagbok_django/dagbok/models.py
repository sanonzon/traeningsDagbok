from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# class Workout_type(models.Model):
    #~ workout_type = models.Selection([('1','Gym'),('2', 'Simning')],string='Workout type')
    # workout_type = (('1', 'Gym'),('2','Simning'))


class Workout_gym(models.Model):
    gym_type = models.CharField(max_length=100)
    gym_sets = models.IntegerField(default=0)
    gym_reps = models.IntegerField(default=0)

class Swimming(models.Model):
    swimdate = models.CharField(max_length=100)
    swimrange = models.IntegerField(default=0)
    swimtime = models.IntegerField(default=0)
    swimfeel = models.CharField(max_length=100)
