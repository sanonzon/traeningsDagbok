#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request, 'dagbok/index.html')

#~ def register(request):
    #~ return HttpResponse("REGISTRERA SIG")

def login(request):
    return HttpResponse("LOGGA IN")

def dashboard(request):
    return render(request, 'dagbok/dashboard.html')


def register(request):
    if request.method == 'POST':
        if request.POST['username'] and request.POST['password']:
            User.objects.create_user(request.POST['username'], 'null@null.com', request.POST['password'])
            
            return HttpResponse("REGISTRERAD fixa annan forward eller nåt<a href='/'>TIllbaka</a>")
    else:
        return render(request, 'dagbok/index.html')
        
        
