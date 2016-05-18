# coding=utf-8

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Workout_gym

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

    passwordRepeat = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=4)

    def clean_username(self):
        #Check if the username is already taken.
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(u"Användarnamnet %s är upptaget." % username)
        return username

    def clean_passwordRepeat(self):
        #Check if the password was repeated, and if the repeated password is a match.
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('passwordRepeat')

        if not password2:
            raise forms.ValidationError(u"Du måste repetera ditt lösenord")
        if password1 != password2:
            raise forms.ValidationError(u"De angivna lösenorden matchar inte varandra.")
        return password2

class LoginAccountForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_password(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        
        user = authenticate(username=username, password=password)

        if user is not None:
            if not user.is_active:
                raise forms.ValidationError(u"Ditt konto är avaktiverat.")
        else:
            raise forms.ValidationError(u"Fel inloggning.")
        
        return password
        

