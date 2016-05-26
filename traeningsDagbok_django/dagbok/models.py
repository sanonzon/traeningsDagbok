# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

from django.utils.encoding import python_2_unicode_compatible
from django.forms import widgets


# Create your models here.

# class Workout_type(models.Model):
    #~ workout_type = models.Selection([('1','Gym'),('2', 'Simning')],string='Workout type')
    # workout_type = (('1', 'Gym'),('2','Simning'))



# TODO en model per workout



@python_2_unicode_compatible
class WorkOuts(models.Model):
    workoutDateNow = models.DateTimeField(auto_now_add=True)
    
    workoutSport = models.CharField(
        max_length=100, 
        choices=(
            ('Loepning', 'Loepning'), 
            ('Simning', 'Simning'), 
            ('Styrketraening', 'Styrketraening')
        ),
    )
    
    workoutFeel = models.CharField(max_length=100,blank=True,null=True)
    workoutUser = models.ForeignKey(User)
    workoutStretch = models.FloatField(blank=True,null=True)
    workoutTime = models.IntegerField(blank=True,null=True)
    workoutSec = models.IntegerField(blank=True,null=True)
    gym_type = models.CharField(max_length=100)
    gym_weight = models.CharField(max_length=100)
    puls = models.IntegerField(blank=True,null=True)
    snittpuls = models.IntegerField(blank=True,null=True)
    minpuls = models.IntegerField(blank=True,null=True)
    kalorier = models.IntegerField(blank=True,null=True)
    
    def __str__(self):
        return "%s - %s - %s" % (str(self.workoutDateNow)[:16], self.workoutSport, self.workoutUser.username)
        
@python_2_unicode_compatible
class UserExtended(models.Model):
    user_id = models.ForeignKey(User)
    city = models.CharField(max_length=100,blank=True,null=True)
    favorite_sport = models.CharField(max_length=100,blank=True,null=True)
    
    def __str__(self):
        return self.user_id.username
    
#~ @python_2_unicode_compatible
#~ class GymWorkout(models.Model):
    #~ title = models.CharField(max_length=100)
    
    #~ def __str__(self):
        #~ return self.title
