# coding=utf-8

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.forms import ModelForm
#~ from .models import GymWorkout

#~ from .models import Workout_gym

class CreateAccountForm(forms.Form):
    #TODO: Se om man kan ändra så att validation erroret som returneras
    #      från forms.CharField kan stå på svenska för att undvika en blandning
    #      av engelska och svenska på sidan.

    username = forms.CharField(
            min_length=2,
            max_length=30,
            widget=forms.TextInput(attrs = {
                'class': 'form-control',
                'placeholder': 'Anv\xC3\xA4ndarnamn',
            })
        )

    password = forms.CharField(
            min_length=4,
            widget=forms.PasswordInput(attrs = {
                'class': 'form-control',
                'placeholder': 'L\xC3\xB6senord',
            })
        )

    passwordRepeat = forms.CharField(
            min_length=4,
            widget=forms.PasswordInput(attrs = {
                'class': 'form-control',
                'placeholder': 'L\xC3\xB6senord igen',
            })
        )

    def clean_username(self):
        #Check if the username is already taken.
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(u"Anv\xC3\xA4ndarnamnet %s \xC3\xA4r upptaget." % username)
        return username

    def clean_passwordRepeat(self):
        #Check if the password was repeated, and if the repeated password is a match.
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('passwordRepeat')

        if not password2:
            raise forms.ValidationError(u"Du m\xC3\xA5ste repetera ditt l\xC3\xB6senord")
        if password1 != password2:
            raise forms.ValidationError(u"De angivna l\xC3\xB6senorden matchar inte varandra.")
        return password2

class LoginAccountForm(forms.Form):

    username = forms.CharField(
            widget=forms.TextInput(attrs = {
                'class': 'form-control',
                'placeholder': 'Anv\xC3\xA4ndarnamn',
            })
        )

    password = forms.CharField(
            widget=forms.PasswordInput(attrs = {
                'class': 'form-control',
                'placeholder': 'L\xC3\xB6senord',
            })
        )

    def clean_password(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if not user.is_active:
                raise forms.ValidationError(u"Ditt konto \xC3\xA4r avaktiverat.")
        else:
            raise forms.ValidationError(u"Fel inloggning.")

        return password

class WorkoutRegisterForm(forms.Form):
    date = forms.DateField()
    
    stretch = forms.IntegerField(label="Sträcka",
            widget=forms.TextInput(attrs = {
                'class': 'form-control',
                'placeholder': 'T.ex. 50',
                'aria-describedby': 'basic-addon2',
            })
        )

    time = forms.CharField(label="Tid",
            widget=forms.TimeInput(attrs = {
                'class': 'form-control',
                'placeholder': 'T.ex. 3',
                'aria-describedby': 'basic-addon2',
            })
        )

    feeling = forms.CharField(label="Känsla",
            max_length = 500,
            widget=forms.TextInput(attrs = {
                'class': 'form-control fastWorkoutFeeling',
                'placeholder': 'Hur k\xC3\xA4ndes det?',
            })
        )

    gym_weight = forms.CharField(label="Vikt",
            widget=forms.TextInput(attrs = {
                'class': 'form-control',
                'placeholder': 'T.ex. 120.5',
                'aria-describedby': 'basic-addon2',
            })
        )

    gym_type = forms.CharField(label="Övning",
            max_length = 100,
            widget=forms.TextInput(attrs = {
                'class': 'form-control',
                'placeholder': 'T.ex. Squats',
                'aria-describedby': 'basic-addon2',
            })
        )
    gym_reps = forms.CharField(label="Reps",
            max_length = 100,
            widget=forms.TextInput(attrs = {
                'class': 'form-control',
                'placeholder': 'Repetitioner',
                'aria-describedby': 'basic-addon2',
            })
        )
    gym_sets = forms.CharField(label="Övning",
            max_length = 100,
            widget=forms.TextInput(attrs = {
                'class': 'form-control',
                'placeholder': 'Set',
                'aria-describedby': 'basic-addon2',
            })
        )

    #~ def clean_time(self):
        #~ time = self.cleaned_data['time'].split(':')
        #~
        #~ if len(time) == 1:
            #~ if time[0].isdigit():
                #~ time.append(0)
            #~ else:
                #~ forms.ValidationError(u'Felaktig inmatning.')
        #~ elif len(time) == 2:
            #~ if not time[0].isdigit() and not time[1].isdigit():
                #~ forms.ValidationError(u'Felaktig inmatning.')
#~
        #~ return time

class SearchForm(forms.Form):
    search = forms.CharField(
            max_length = 100,
            widget=forms.TextInput(attrs = {
                'class': 'form-control',
                'placeholder': 'S\xC3\xB6k anv\xC3\xA4ndarnamn',
            }))

class AdvancedWorkout(forms.Form):
    date = forms.DateField()
    
    puls = forms.IntegerField(label="Maximal Puls",
            widget=forms.TextInput(attrs = {
                'class': 'form-control',
                'placeholder': 'Maximal puls',
            }))

    snittpuls = forms.FloatField(label="Snittpuls",
            widget=forms.TextInput(attrs = {
                'class': 'form-control',
                'placeholder': 'Snittpuls',
            }))

    minpuls = forms.IntegerField(label="Minimal puls",
            widget=forms.TextInput(attrs = {
                'class': 'form-control',
                'placeholder': 'Minimal puls',
            }))

    kalorier = forms.IntegerField(label="Kalorier",
            widget=forms.TextInput(attrs = {
                'class': 'form-control',
                'placeholder': 'Kalorier',
            }))
