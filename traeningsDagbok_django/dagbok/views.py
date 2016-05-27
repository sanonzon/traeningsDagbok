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

from .forms import CreateAccountForm, LoginAccountForm, WorkoutRegisterForm, SearchForm, AdvancedWorkout
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
                create_extended_user(request,user)
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
        #~ gym_type_form = GymWorkoutForm()
        WRF = WorkoutRegisterForm(request.POST)
        WorkOut = WorkOuts()

        if request.POST:
            stretch = request.POST['stretch']
            if (len(stretch) > 0 and stretch.isdigit()) or len(request.POST['time']):
                if not len(stretch) > 0:
                    streckan_fixed = "0"
                else:
                    streckan_fixed = ""
                    for c in stretch:
                        if (c == "," or c == ".") and not "." in streckan_fixed:
                            streckan_fixed += "."
                        elif c.isdigit():
                            streckan_fixed += c

                if not len(streckan_fixed) > 0:
                    streckand_fixed = "0"

                if request.POST['workoutType'] == 'weightlifting':
                    if request.POST['time'].isdigit():
                        WorkOut.gym_type = request.POST['gym_type']
                        WorkOut.gym_weight = request.POST['gym_weight']
                        WorkOut.workoutFeel = request.POST['feeling']
                        WorkOut.workoutStretch = stretch
                        WorkOut.workoutTime = request.POST['time']
                        WorkOut.workoutUser = User.objects.filter(id=request.user.id).get()
                        WorkOut.workoutSport = u"Styrketraening"
                        WorkOut.workoutSec = 0
                        WorkOut.save()
                    else:
                        return HttpResponseRedirect("/dashboard")

                elif request.POST['workoutType'] == 'swimming':
                    tiden = request.POST['time'].split(":")

                    if tiden[0].isdigit() and (len(tiden) == 1 or tiden[1].isdigit()):
                        if len(tiden) == 1:
                            tiden.append(0)
                    else:
                        tiden = [0, 0]

                    WorkOut.workoutTime = tiden[0]
                    WorkOut.workoutSec = tiden[1]
                    WorkOut.workoutFeel = request.POST['feeling']
                    WorkOut.workoutStretch = streckan_fixed
                    WorkOut.workoutUser = User.objects.filter(id=request.user.id).get()
                    WorkOut.workoutSport = u"Simning"
                    WorkOut.save()

                elif request.POST['workoutType'] == 'running':
                    tiden = request.POST['time'].split(":")

                    if tiden[0].isdigit() and (len(tiden) == 1 or tiden[1].isdigit()):
                        if len(tiden) == 1:
                            tiden.append(0)
                    else:
                        tiden = [0, 0]

                    WorkOut.workoutTime = tiden[0]
                    WorkOut.workoutSec = tiden[1]
                    WorkOut.workoutFeel = request.POST['feeling']
                    WorkOut.workoutStretch = streckan_fixed
                    WorkOut.workoutUser = User.objects.filter(id=request.user.id).get()
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

    given_id = None

    if request.POST:
        given_id = request.POST['given_id']

    events = WorkOuts.objects.filter(workoutUser = request.user.id).order_by('workoutDateNow')
    workout = WorkOuts.objects.filter(id = given_id)

    if workout:
        workout = workout[0]

    calendar = []

    if events:
        for event in events:
            calendar.append({
                'id': event.id,
                'title': event.workoutSport,
                'start': event.workoutDateNow.replace(microsecond = 0).isoformat(),
                #~ 'end': event.workoutDateNow.replace(microsecond = 0).isoformat(),
            })

    if request.is_ajax():
        html = loader.render_to_string('dagbok/workoutmodal.html', {
                'workout': workout,
            })
        return HttpResponse(html)
    else:
        return render(request, 'dagbok/calendar.html', {
                'workout_calendar': json.dumps(calendar),
            })

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
    match = re.search(r'GET \'\/user\/([\w\d]+)\/?\'', str(request))

    if match:
        #~ print match.group(1)
        if User.objects.filter(username=match.group(1)):
            user = User.objects.filter(username=match.group(1)).get()
            url_user_id = User.objects.filter(id=user.id).values_list('id', flat=True)[0]
            #~ print ("url_user_id : %s") % url_user_id

            if UserExtended.objects.filter(user_id=url_user_id):
                user_extended = UserExtended.objects.filter(user_id=url_user_id).get()
            else:
                user_extended = None

            #~ print ("user_extended object finns?: %s") % user_extended


            if len(user.first_name) > 0 and len(user.last_name) > 0:
                hack_dict = {'full_name': " ".join([user.first_name, user.last_name])}
            else:
                hack_dict = {'full_name': user.username}
            #~ print user.first_name

            #~ print WorkOuts.objects.filter(workoutUser = url_user_id)

        
            
            if user_extended:
                tmp = []
                for buddy in str(user_extended.buddies).split(","):
                    if buddy.isdigit():
                        tmp += User.objects.values('username').filter(id=buddy)
                print tmp
                
                buddies = [x['username'] for x in tmp]
                #~ buddies = None

                return render(request, 'dagbok/user.html', {
                    'user': user,
                    'full_name': hack_dict,
                    'total_workouts': len(WorkOuts.objects.filter(workoutUser = url_user_id)),
                    'extended': user_extended,
                    'sports': str(user_extended.favorite_sport).lower().replace(" ", "").split(","),
                    'buddies': buddies,
                    })
            else:
                return render(request, 'dagbok/user.html', {
                'user': user,
                'full_name': hack_dict,
                'total_workouts': len(WorkOuts.objects.filter(workoutUser = url_user_id)),
                'extended': None,
                'sports': None,
                'buddies': None,
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
        
        create_extended_user(request,user)
        
        login(request, authenticate(username=username, password=password))
        return redirect('/dashboard')
    else:
        return redirect('/')
        
def create_extended_user(request, user):
    if UserExtended.objects.filter(user_id=user.id):
        pass
    else:
        user_extended = UserExtended()
        user_extended.user_id=User.objects.filter(id=user.id).get()
        user_extended.city=""
        user_extended.favorite_sport=""
        user_extended.buddies=""
        user_extended.save()
    return
    
def update_user(request):
    #~ firstname        lastname        email        new_password        new_password_repeat        current_password
    if request.POST:
        user = authenticate(username=request.POST['username'], password=request.POST['current_password'])

        if authenticate(username=request.POST['username'], password=request.POST['current_password']):
            user = authenticate(username=request.POST['username'], password=request.POST['current_password'])

            if UserExtended.objects.filter(user_id=user.id):
                extended = UserExtended.objects.filter(user_id=user.id).get()
            else:
                extended = UserExtended()
                extended.user_id = User.objects.filter(id=user.id).get()

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



def advanced_workout(request):
    if request.POST:
        WorkOut = WorkOuts()
        #~ <QueryDict: {
        #~ u'kalorier': [u'7'],
         #~ u'stretch': [u'97'],
          #~ u'snittpuls': [u'2'],
           #~ u'workoutType': [u'running'],
            #~ u'time': [u'7'], 
            #~ u'minpuls': [u'77'], 
            #~ u'csrfmiddlewaretoken': [u'Rr7D9DZiWbY4ky9t2bAQLFbb8E9pYmcM'],
             #~ u'feeling': [u'7'],
              #~ u'puls': [u'7']}>
        if request.POST['workoutType'] == "running":
            WorkOut.workoutSport = u"Loepning"
        
        elif request.POST['workoutType'] == "swimming":
            WorkOut.workoutSport = u"Simning"
        
        elif request.POST['workoutType'] == "weightlifting":
            WorkOut.workoutSport = u"Styrketraening"
            WorkOut.gym_type = request.POST['gym_type']
            WorkOut.gym_weight = request.POST['gym_weight']
        else:
            return redirect("/dashboard")
        
        
        WorkOut.puls = request.POST['puls']
        WorkOut.snittpuls = request.POST['snittpuls']
        WorkOut.minpuls = request.POST['minpuls']        
        WorkOut.kalorier = request.POST['kalorier']
        
        WorkOut.workoutFeel = request.POST['feeling']
        WorkOut.workoutStretch = request.POST['stretch']

        if len(request.POST['time']) > 0 and ":" in request.POST['time']:
            tiden = request.POST['time'].split(":")
            if tiden[0].isdigit() and (len(tiden) == 1 or tiden[1].isdigit()):
                if len(tiden) == 1:
                    tiden.append(0)
                else:
                    tiden = [0, 0]
        else:
            tiden = [0, 0]
        WorkOut.workoutTime = tiden[0]
        WorkOut.workoutSec = tiden[0]
        WorkOut.workoutUser = User.objects.filter(id=request.user.id).get()
        
        WorkOut.save()

        print request.POST
        return redirect("/advanced_workout")
    else:
        return render(request, "dagbok/advanced_workout.html",{'advanced_workout_form':AdvancedWorkout(),'WRF': WorkoutRegisterForm()})

def add_buddy(request):
    if request.POST:        
        user_extended = UserExtended.objects.filter(user_id=request.user.id).get()

        if len(user_extended.buddies) > 0:
            if request.POST['get_buddy'] not in user_extended.buddies:
                user_extended.buddies = user_extended.buddies + request.POST['get_buddy'] + ","
        else:
            user_extended.buddies = request.POST['get_buddy'] + ","
            
        
        
        user_extended.save()
        return redirect("/user/"+request.user.username)
        
    else:
        return redirect("/dashboard")
        
        
        
        

