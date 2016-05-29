# coding=utf-8

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.forms import ModelForm
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title','text']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
