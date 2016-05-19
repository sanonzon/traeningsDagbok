#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

import json
from .forms import CreateAccountForm, LoginAccountForm, WorkoutRegisterForm
from .models import WorkOuts

# Create your views here.
def index(request):
    register_form = CreateAccountForm(request.POST)
    login_form = LoginAccountForm(request.POST)
    return render(
        request,
        'dagbok/index.html',
        {
            'register_form': register_form,
            'login_form': login_form,
        })

def login_user(request):
    form = LoginAccountForm(request.POST)

    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                #~ return render(request, 'dagbok/dashboard.html')
                return redirect('/dashboard')
                # Redirect to a success page.
            else:
                return redirect('/')
                # Return a 'disabled account' error message
        else:
            return redirect('/')
            # Return an 'invalid login' error message.
    else:
        return redirect('/')

def logout_user(request):
    logout(request)
    return redirect('/')
    #~ return render(request, 'dagbok/index.html')

def dashboard(request):

    WRF = WorkoutRegisterForm(request.POST)
    WorkOut = WorkOuts()

    if request.POST:
        print request.POST

        if request.POST['workoutType'] == 'weightlifting':
            WorkOut.workoutFeel = request.POST['feeling']
            WorkOut.workoutUser = request.user.id
            WorkOut.workoutSport = u"Styrketraening"
            WorkOut.save()
        elif request.POST['workoutType'] == 'swimming':
            WorkOut.workoutFeel = request.POST['feeling']
            WorkOut.workoutUser = request.user.id
            WorkOut.workoutSport = u"Simning"
            WorkOut.save()
        elif request.POST['workoutType'] == 'running':
            WorkOut.workoutFeel = request.POST['feeling']
            WorkOut.workoutUser = request.user.id
            WorkOut.workoutSport = u"Loepning"
            WorkOut.save()

    return render(request, 'dagbok/dashboard.html', {
            'WRF': WRF,
            'workouts': WorkOuts.objects.filter(workoutUser = request.user.id).order_by('-workoutDateNow')[:5]
        })

def header(request):
    return render(request, 'dagbok/header.html')

def footer(request):
    return render(request, 'dagbok/footer.html')

def calendar(request):
    return render(request, 'dagbok/calendar.html')

def profile(request):
    return render(request, 'dagbok/profile.html')

def create_user(request):
    form = CreateAccountForm(request.POST)

    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = User(username=username)
        user.set_password(password)
        user.is_active = True
        user.save()

        login(request, authenticate(username=username, password=password))
        return redirect('/dashboard')
    else:
        return redirect('/')
