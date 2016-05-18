#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
# from django.template import RequestContext
from django.shortcuts import render_to_response
from . import models

import json
from .forms import CreateAccountForm, LoginAccountForm

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
    print request.POST
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
    # context = RequestContext(request)
    swimmingFastWork = models.Swimming.objects.all()
    workouts = models.WorkOuts.objects.all().order_by('-id')[:5]
    return render_to_response('dagbok/dashboard.html', {'workouts': workouts})

def header(request):
    return render(request, 'dagbok/header.html')

def footer(request):
    return render(request, 'dagbok/footer.html')

def calendar(request):
    return render(request, 'dagbok/calendar.html')

def profile(request):
    return render(request, 'dagbok/profile.html')

def register(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            User.objects.create_user(username, 'null@null.com', password)

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/dashboard')

        if form.is_valid():
            print "Form is valid."
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User(username=username)
            user.set_password(password)
            user.is_active = True
            user.save()

            login(request, authenticate(username=username, password=password))
            return redirect('/dashboard')
        else:
            print "form is not valid"
            errors = form.errors
            return redirect('/')
    else:
        return redirect('/')




