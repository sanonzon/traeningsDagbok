# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

from django.utils.encoding import python_2_unicode_compatible
from django.forms import widgets



@python_2_unicode_compatible
class Category(models.Model):
    choices =  [
            ('Löpning', 'Löpning'), 
            ('Simning', 'Simning'), 
            ('Styrketräning', 'Styrketräning')
        ]
        
    def __str__(self):
        return self.category
        
@python_2_unicode_compatible
class Post(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User)
    category = models.CharField(
        max_length=100, 
        choices=Category.choices
        )
    text = models.TextField(max_length=255,default="")
    
    def __str__(self):
        return "%s - %s - %s - %s" %(self.date, self.title, self.category, self.author.username)


@python_2_unicode_compatible
class Comment(models.Model):
    date = models.DateTimeField(auto_now_add=True)    
    author = models.ForeignKey(User)
    postParent = models.ForeignKey(Post)
    text = models.TextField(default="")


    def __str__(self):
        return "%s - %s - %s" %(self.date, self.author.username, self.postParent.title)


