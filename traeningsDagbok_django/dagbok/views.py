#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

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
        
        
