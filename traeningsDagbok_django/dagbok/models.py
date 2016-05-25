# -*- coding: utf-8 -*-

#~ from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.

# class Workout_type(models.Model):
    #~ workout_type = models.Selection([('1','Gym'),('2', 'Simning')],string='Workout type')
    # workout_type = (('1', 'Gym'),('2','Simning'))


@python_2_unicode_compatible
class WorkOuts(models.Model):
    workoutDateNow = models.DateTimeField(auto_now_add=True)
    workoutSport = models.CharField(max_length=100)
    workoutFeel = models.CharField(max_length=100)
    workoutUser = models.ForeignKey(User)
    workoutStretch = models.FloatField()
    workoutTime = models.IntegerField()
    workoutSec = models.IntegerField()
    gym_type = models.ForeignKey('GymWorkout')
    gym_weight = models.CharField(max_length=100)
    
    def __str__(self):
        return "%s - %s - %s" % (str(self.workoutDateNow)[:16], self.workoutSport, self.workoutUser.username)
        
@python_2_unicode_compatible
class UserExtended(models.Model):
    user_id = models.ForeignKey(User)
    city = models.CharField(max_length=100)
    favorite_sport = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user_id.username
    
@python_2_unicode_compatible
class GymWorkout(models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title
