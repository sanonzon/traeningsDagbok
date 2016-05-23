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
from .models import WorkOuts, UserExtended


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
                if request.POST['stretch'].isdigit() and request.POST['time'].isdigit():
                    if request.POST['workoutType'] == 'weightlifting':
                        WorkOut.gym_type = request.POST['gym_type']
                        WorkOut.gym_weight = request.POST['gym_weight']
                        WorkOut.workoutFeel = request.POST['feeling']
                        WorkOut.workoutStretch = request.POST['stretch']
                        WorkOut.workoutTime = request.POST['time']
                        WorkOut.workoutUser = request.user.id
                        WorkOut.workoutSport = u"Styrketraening"
                        WorkOut.save()
                    else:
                        return HttpResponseRedirect("/dashboard")

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
            else:
                return HttpResponseRedirect("/dashboard")
        return render(request, 'dagbok/dashboard.html', {
                'WRF': WorkoutRegisterForm(),
                'workouts': WorkOuts.objects.filter(workoutUser = request.user.id).order_by('-workoutDateNow')[:5],
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
    user_extended = UserExtended.objects.filter(user_id=request.user.id).get()
    

    print "DENNA STRÄNGEN JOBBAR VI MED: %s" %str(request)

    match = re.search(r'GET \'\/user\/([\w\d]+)\'', str(request))

    print match

    match = re.search(r'GET \'\/user\/([\w\d]+)\/?\'', str(request))

    if match:
        print match.group(1)
        if User.objects.filter(username=match.group(1)):
            user = User.objects.filter(username=match.group(1)).get()
            
            if len(user.first_name) > 0 and len(user.last_name) > 0:
                hack_dict = {'full_name': " ".join([user.first_name, user.last_name])}
            else:
                hack_dict = {'full_name': user.username}
            print user.first_name
            return render(request, 'dagbok/user.html', {
                'user': user,
                'full_name': hack_dict,
                'total_workouts': len(WorkOuts.objects.filter(workoutUser = request.user.id)),
                'extended': user_extended,
                'sports':str(user_extended.favorite_sport).lower().replace(" ", "").split(",")
                })
        else:
            return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponseRedirect('/dashboard')

def searched(request):
    if request.POST:
        results =  User.objects.filter(username__contains=request.POST['search'])
        return render(request, 'dagbok/profile.html', {'results': results})
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

def update_user(request):
    #~ firstname        lastname        email        new_password        new_password_repeat        current_password
    if request.POST:        
        user = authenticate(username=request.POST['username'], password=request.POST['current_password'])
   
        if authenticate(username=request.POST['username'], password=request.POST['current_password']):
            user = authenticate(username=request.POST['username'], password=request.POST['current_password'])
            extended = UserExtended.objects.filter(user_id=user.id).get()
            
            sports = ""
            if "swim" in request.POST:
                sports += "swim,"
            
            if "gym" in request.POST:
                sports += "gym,"
            
            if "run" in request.POST:
                sports += "run,"
            
     
            
            if len(request.POST['firstname']) > 0:
                user.first_name = request.POST['firstname']
            if len(request.POST['lastname']) > 0:
                user.last_name = request.POST['lastname']
            if len(request.POST['email']) > 0:
                user.email = request.POST['email']
            if len(request.POST['new_password']) > 0 and request.POST['new_password'] == request.POST['new_password_repeat']:
                user.set_password(request.POST['new_password'])
            if len(sports) > 0:
                extended.favorite_sport = sports
            if len(request.POST['city']) > 0:
                extended.city = request.POST['city']
            
            extended.save()
            user.save()
            return redirect("/dashboard")
        else:
            return redirect("/")
        
    else:
        return redirect("/")

        
