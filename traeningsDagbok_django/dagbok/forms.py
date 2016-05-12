# coding=utf-8

from django import forms
from django.contrib.auth.models import User


class CreateAccountForm(forms.Form):
    #TODO: Se om man kan ändra så att validation erroret som returneras 
    #      från forms.CharField kan stå på svenska för att undvika en blandning
    #      av engelska och svenska på sidan.

    username = forms.CharField(
        min_length=2,
        max_length=30)

    password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=4)

    def clean_username(self):
        #Check if the username is already taken.
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                u"Användarnamnet %s upptaget" % username)
        return username
