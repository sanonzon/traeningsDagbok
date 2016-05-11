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
        print request.POST        
        #~ userName = request.REQUEST.get('username', None)
        #~ userPass = request.REQUEST.get('password', None)
        #~ userMail = request.REQUEST.get('email', None)
        
        #~ user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

        #~ username = request.POST['username']
        #~ password = request.POST['password']
        return HttpResponse("REGISTRERA SIG")
    else:
        return render(request, 'dagbok/index.html')
        
        
