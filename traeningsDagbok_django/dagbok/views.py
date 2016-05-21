#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import loader
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse

import json
import re

from .forms import CreateAccountForm, LoginAccountForm, WorkoutRegisterForm, SearchForm
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
    if request.user.is_authenticated():
        WRF = WorkoutRegisterForm(request.POST)
        WorkOut = WorkOuts()

        if request.POST:
            if len(request.POST['stretch']) > 0 or len(request.POST['time']):
                if request.POST['workoutType'] == 'weightlifting':
                    WorkOut.workoutFeel = request.POST['feeling']
                    WorkOut.workoutStretch = request.POST['stretch']
                    WorkOut.workoutTime = request.POST['time']
                    WorkOut.workoutUser = request.user.id
                    WorkOut.workoutSport = u"Styrketraening"
                    WorkOut.save()
                elif request.POST['workoutType'] == 'swimming':
                    WorkOut.workoutFeel = request.POST['feeling']
                    WorkOut.workoutStretch = request.POST['stretch']
                    WorkOut.workoutTime = request.POST['time']
                    WorkOut.workoutUser = request.user.id
                    WorkOut.workoutSport = u"Simning"
                    WorkOut.save()
                elif request.POST['workoutType'] == 'running':
                    WorkOut.workoutFeel = request.POST['feeling']
                    WorkOut.workoutStretch = request.POST['stretch']
                    WorkOut.workoutTime = request.POST['time']
                    WorkOut.workoutUser = request.user.id
                    WorkOut.workoutSport = u"Loepning"
                    WorkOut.save()

                return HttpResponseRedirect("/dashboard")

        return render(request, 'dagbok/dashboard.html', {
                'WRF': WorkoutRegisterForm(),
                'workouts': WorkOuts.objects.filter(workoutUser = request.user.id).order_by('-workoutDateNow')[:5]
            })
    else:
        return HttpResponseRedirect("/")

def header(request):
    return render(request, 'dagbok/header.html')

def footer(request):
    return render(request, 'dagbok/footer.html')

def calendar(request):
    return render(request, 'dagbok/calendar.html')

def profile(request):
    if request.POST:
        return render(request, 'dagbok/profile.html', {
        'searchForm': SearchForm(),
        'results': User.objects.filter(username__contains=request.POST['search'])
        })

    return render(request, 'dagbok/profile.html', {
    'searchForm': SearchForm(),
    })

def user(request):
    #~ GET '/user/axeasd22232l/'
    print "DENNA STRÄNGEN JOBBAR VI MED: %s" %str(request)

    match = re.search(r'/user/([\w\d]+)/', str(request)).group(1) or None

    if match:
        user = User.objects.all().filter(username=match) or None
        if user:
            return render(request, 'dagbok/user.html', {'user':user})
        else:
            return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponseRedirect('/dashboard')

def searched(request):
    if request.POST:
        if request.POST['search'] == '':
            return HttpResponseRedirect('/dashboard')
        #~ url = 'user/%s' % request.POST['search']
        return HttpResponseRedirect('/user/%s' % request.POST['search'])
    else:
        return HttpResponseRedirect('/dashboard')

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
