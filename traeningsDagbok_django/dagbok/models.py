#~ from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# class Workout_type(models.Model):
    #~ workout_type = models.Selection([('1','Gym'),('2', 'Simning')],string='Workout type')
    # workout_type = (('1', 'Gym'),('2','Simning'))


class WorkOuts(models.Model):
    workoutDateNow = models.DateTimeField(auto_now_add=True)
    workoutSport = models.CharField(max_length=100)
    workoutFeel = models.CharField(max_length=100)
    workoutUser = models.IntegerField()
    
    def __str__(self):
        return self.workoutSport



class Workout_gym(WorkOuts):
    gym_type = models.CharField(max_length=100)
    gym_sets = models.IntegerField(default=0)
    gym_reps = models.IntegerField(default=0)

class Swimming(WorkOuts):
    swimrange = models.IntegerField(default=0)
    swimtime = models.IntegerField(default=0)

