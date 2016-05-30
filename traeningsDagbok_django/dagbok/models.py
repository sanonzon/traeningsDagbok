# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

from django.utils.encoding import python_2_unicode_compatible
from django.forms import widgets



@python_2_unicode_compatible
class WorkOuts(models.Model):
    workoutDateNow = models.DateTimeField()

    workoutSport = models.CharField(
        max_length=100,
        choices=(
            ('Loepning', 'Loepning'),
            ('Simning', 'Simning'),
            ('Styrketraening', 'Styrketraening')
        ),
    )
    #~ workoutCustomDate = models.DateTimeField(blank=True,null=True)
    workoutFeel = models.CharField(max_length=100,blank=True,null=True)
    workoutUser = models.ForeignKey(User)
    workoutStretch = models.FloatField(blank=True,null=True)
    workoutTime = models.IntegerField(blank=True,null=True)
    workoutSec = models.IntegerField(blank=True,null=True)
    gym_type = models.CharField(blank=True,max_length=100)
    gym_weight = models.FloatField(blank=True,default=0)
    gym_sets = models.IntegerField(blank=True,default=0)
    gym_reps = models.IntegerField(blank=True,default=0)
    puls = models.IntegerField(blank=True,null=True)
    snittpuls = models.FloatField(blank=True,null=True)
    minpuls = models.IntegerField(blank=True,null=True)
    kalorier = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return "%s - %s - %s" % (str(self.workoutDateNow)[:16], self.workoutSport, self.workoutUser.username)

@python_2_unicode_compatible
class UserExtended(models.Model):
    user_id = models.ForeignKey(User)
    city = models.CharField(max_length=100,default="")
    favorite_sport = models.CharField(max_length=100,default="")
    buddies = models.CharField(max_length=255,default="")
    picture = models.CharField(max_length=255,default="")

    def __str__(self):
        return "%s - %s" %(self.user_id.username, self.user_id.id)

@python_2_unicode_compatible
class TotalWorkouts(models.Model):
    user_id = models.ForeignKey(User)
    total_workouts = models.IntegerField(default=-1)

    def save(self):
        self.total_workouts += 1
        super(TotalWorkouts, self).save()

    def __str__(self):
        return "%s - %s" %(self.user_id.username, self.total_workouts)
        
        
@python_2_unicode_compatible
class Goals(models.Model):
    user_id = models.ForeignKey(User)
    workoutDateNow = models.DateTimeField()
    goalWeight = models.FloatField(default=0)
    currentWeight = models.FloatField(default=0)
    
    def __str__(self):
        return "%s - %s - %s" % (self.user_id.username,self.goalWeight,self.currentWeight)
    
    
