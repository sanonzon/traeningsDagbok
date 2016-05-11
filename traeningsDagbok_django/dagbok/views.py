from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


# Create your views here.
def index(request):
    return render(request, 'dagbok/index.html')

def register(request):
    return HttpResponse("REGISTRERA SIG")

def login(request):
    return HttpResponse("LOGGA IN")

def dashboard(request):
    return render(request, 'dagbok/dashboard.html')
