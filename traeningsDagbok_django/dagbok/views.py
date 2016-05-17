#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

from .forms import CreateAccountForm

# Create your views here.
def index(request):
    return render(request, 'dagbok/index.html')

#~ def register(request):
    #~ return HttpResponse("REGISTRERA SIG")

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            #~ return render(request, 'dagbok/dashboard.html')
            return redirect('/dashboard')
            # Redirect to a success page.
        else:
            return HttpResponse("Disabled account.")
            # Return a 'disabled account' error message
    else:
        return HttpResponse("Invalid login.")
        # Return an 'invalid login' error message.

def logout_user(request):
    logout(request)
    return redirect('/')
    #~ return render(request, 'dagbok/index.html')

def dashboard(request):
    #~ return redirect('/dashboard')
    return render(request, 'dagbok/dashboard.html')

def header(request):
    #~ return redirect('/dashboard')
    return render(request, 'dagbok/header.html')

def footer(request):
    #~ return redirect('/dashboard')
    return render(request, 'dagbok/footer.html')

def calendar(request):
    #~ return redirect('/dashboard')
    return render(request, 'dagbok/calendar.html')

def profile(request):
    #~ return redirect('/dashboard')
    return render(request, 'dagbok/profile.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            User.objects.create_user(username, 'null@null.com', password)

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/dashboard')

            #~ return render(request, 'dagbok/dashboard.html')
            #~ return HttpResponse("REGISTRERAD fixa annan forward eller nåt<a href='/'>TIllbaka</a>")
    else:
        return redirect('/')

def create_user(request):
    #~ if request.user.is_authenticated():
        #~ return redirect('bank-login')

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
        return render(
            request,
            'dagbok/index.html',
            {
                'form': form,
            })
