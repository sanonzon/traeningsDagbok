#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import loader
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.utils import timezone

import json
import re
import datetime

from .forms import CreateAccountForm, LoginAccountForm, WorkoutRegisterForm, SearchForm, AdvancedWorkout
from .models import WorkOuts, UserExtended, TotalWorkouts, Goals

# Create your views here.
def index(request):
    register_form = CreateAccountForm(request.POST)
    login_form = LoginAccountForm(request.POST)

    if register_form.is_valid():
        return create_user(request)
    elif login_form.is_valid():
        return login_user(request)
    else:
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
        #~ gym_type_form = GymWorkoutForm()
        WRF = WorkoutRegisterForm(request.POST)
        WorkOut = WorkOuts()

        if request.POST:
            if request.POST['workoutType'] == 'weightlifting':
                WorkOut.workoutDateNow = request.POST['date']
                WorkOut.gym_type = request.POST['gym_type']
                if test_float(request.POST['gym_weight']):
                    WorkOut.gym_weight = request.POST['gym_weight']
                if test_integer(request.POST['gym_sets']):
                    WorkOut.gym_sets = request.POST['gym_sets']
                if test_integer(request.POST['gym_reps']):
                    WorkOut.gym_reps = request.POST['gym_reps']
                WorkOut.workoutFeel = request.POST['feeling']
                WorkOut.workoutUser = User.objects.filter(id=request.user.id).get()
                WorkOut.workoutSport = u"Styrketraening"
                WorkOut.save()
                TotalWorkouts.objects.filter(user_id=request.user.id).get().save()

                return redirect("/dashboard")

            elif request.POST['workoutType'] == 'swimming':
                tiden = test_time(request.POST['time'])
                
                WorkOut.workoutDateNow = request.POST['date']
                WorkOut.workoutTime = tiden[0]
                WorkOut.workoutSec = tiden[1]
                WorkOut.workoutFeel = request.POST['feeling']
                if test_float(request.POST['stretch']):
                    WorkOut.workoutStretch = request.POST['stretch']
                WorkOut.workoutUser = User.objects.filter(id=request.user.id).get()
                WorkOut.workoutSport = u"Simning"
                WorkOut.save()
                TotalWorkouts.objects.filter(user_id=request.user.id).get().save()

                return redirect("/dashboard")

            elif request.POST['workoutType'] == 'running':
                tiden = test_time(request.POST['time'])
                
                WorkOut.workoutDateNow = request.POST['date']
                WorkOut.workoutTime = tiden[0]
                WorkOut.workoutSec = tiden[1]
                WorkOut.workoutFeel = request.POST['feeling']
                if test_float(request.POST['stretch']):
                    WorkOut.workoutStretch = request.POST['stretch']
                WorkOut.workoutUser = User.objects.filter(id=request.user.id).get()
                WorkOut.workoutSport = u"Loepning"
                WorkOut.save()
                TotalWorkouts.objects.filter(user_id=request.user.id).get().save()

                return redirect("/dashboard")
            else:
                return HttpResponseRedirect("/dashboard")
        else:
            return render(request, 'dagbok/dashboard.html', {
                'WRF': WorkoutRegisterForm(),
                'workouts': WorkOuts.objects.filter(workoutUser = request.user.id).order_by('-id')[:5],
                })
    else:
        return redirect("/")

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
            url_user = User.objects.filter(username=match.group(1)).get()
            url_user_extended = UserExtended.objects.filter(user_id=url_user.id).get()

            if len(url_user.first_name) > 0 and len(url_user.last_name) > 0:
                hack_dict = {'full_name': " ".join([url_user.first_name, url_user.last_name])}
            else:
                hack_dict = {'full_name': url_user.username}

            logged_in_user_extended = UserExtended.objects.filter(user_id=request.user.id).get()

            buddy_ids = []
            tmp = []
            for buddy in str(logged_in_user_extended.buddies).split(","):
                if buddy.isdigit():
                    tmp += User.objects.values('username').filter(id=buddy)
                    buddy_ids.append(int(buddy))
            
            buddies_pic = []
            buddy_workout = []
            for x in tmp:
                buddies_pic.append(UserExtended.objects.values_list('picture',flat=True).filter(user_id=User.objects.filter(username=x['username']))[0])
                buddy_workout.append(WorkOuts.objects.values_list('workoutDateNow','workoutSport').filter(workoutUser=User.objects.filter(username=x['username'])).order_by('-id')[:1])
            
            buddies = [x['username'] for x in tmp]
            if url_user.id == request.user.id:
                buddy_button = None
            elif url_user.id in buddy_ids:
                buddy_button = None
            else:
                buddy_button = True

            zippat = zip(buddies,buddies_pic,buddy_workout)
            
            print zippat

            print buddy_workout 
            
            return render(request, 'dagbok/user.html', {
                'user': url_user,
                'full_name': hack_dict,
                'total_workouts': TotalWorkouts.objects.filter(user_id=url_user.id).values_list('total_workouts',flat=True)[0],
                'extended': url_user_extended,
                'sports': str(url_user_extended.favorite_sport).lower().replace(" ", "").split(","),
                'zippat': zippat,
                'buddy_button': buddy_button,
                })
        else:
            return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponseRedirect('/dashboard')

def searched(request):
    if request.POST:
        results =  User.objects.filter(username__icontains=request.POST['search'])
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

        UserExtended(user_id=user).save()
        TotalWorkouts(user_id=user).save()
        Goals(user_id=user).save()

        login(request, authenticate(username=username, password=password))
        return redirect('/dashboard')
    else:
        return render(
                request,
                'dagbok/index.html', {
                'register_form': form,
            })

def update_user(request):
    #~ firstname        lastname        email        new_password        new_password_repeat        current_password
    if request.POST:
        user = authenticate(username=request.POST['username'], password=request.POST['current_password'])

        if user:

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

            user.first_name = request.POST['firstname']
            user.last_name = request.POST['lastname']
            user.email = request.POST['email']
            extended.picture=request.POST['picture']
            extended.favorite_sport = sports
            extended.city = request.POST['city']

            if len(request.POST['new_password']) > 0 and request.POST['new_password'] == request.POST['new_password_repeat']:
                user.set_password(request.POST['new_password'])

            extended.save()
            user.save()
            return redirect("/dashboard")
        else:
            return redirect("/")

    else:
        return redirect("/")


    return render(request, 'dagbok/gymtest.html', {
                    'form':form
                    })

def goals(request):
    if request.POST:
        timezone.now()
        if test_float(request.POST['viktgoal']) and test_float(request.POST['viktnow']):
                newGoal = Goals()
                newGoal.user_id = User(id=request.user.id)
                newGoal.goalWeight = request.POST['viktgoal']
                newGoal.currentWeight = request.POST['viktnow']
                newGoal.save()
                
        elif test_float(request.POST['viktgoal']):
                newGoal = Goals()
                oldGoals = Goals.objects.filter(user_id=request.user.id).order_by('workoutDateNow')
                newGoal.user_id = User(id=request.user.id)
                newGoal.goalWeight = request.POST['viktgoal']
                newGoal.currentWeight = oldGoals[len(oldGoals) - 1].currentWeight
                newGoal.save()
            
        elif test_float(request.POST['viktnow']):
                newGoal = Goals()
                oldGoals = Goals.objects.filter(user_id=request.user.id).order_by('workoutDateNow')
                newGoal.user_id = User(id=request.user.id)
                newGoal.goalWeight = oldGoals[len(oldGoals) - 1].goalWeight
                newGoal.currentWeight = request.POST['viktnow']
                newGoal.save()
            
        return redirect("/goals")
    else:
        g = Goals.objects.filter(user_id=request.user.id)
        return render(request, 'dagbok/goals.html', {'goals':g})

def forum(request):
    return render(request, 'dagbok/forum.html')

def progress(request):
    getGoals = Goals.objects.filter(user_id=request.user.id).order_by('workoutDateNow')
    if len(getGoals) > 1:
        getGoals = getGoals[1:]

    return render(request, 'dagbok/progress.html',
        {
            'lbls': json.dumps([str(goal.workoutDateNow)[:16] for goal in getGoals]),
            'weightData': json.dumps([goal.currentWeight for goal in getGoals]),
            'goalWeight': json.dumps([goal.goalWeight for goal in getGoals]),
        })

def settings(request):
    sports = str(UserExtended.objects.filter(user_id=request.user.id).get().favorite_sport).lower().replace(" ", "").split(",")
    extended = UserExtended.objects.filter(user_id=request.user.id).get()
    
    return render(request, 'dagbok/settings.html',{'sports':sports, 'extended':extended})

def advanced_workout(request):
    if request.POST:
        WorkOut = WorkOuts()

        if request.POST['workoutType'] == "running":
            WorkOut.workoutSport = u"Loepning"

        elif request.POST['workoutType'] == "swimming":
            WorkOut.workoutSport = u"Simning"

        elif request.POST['workoutType'] == "weightlifting":
            WorkOut.workoutSport = u"Styrketraening"
            WorkOut.gym_type = request.POST['gym_type']
            if test_integer(request.POST['gym_weight']) or test_float(request.POST['gym_weight']):
                WorkOut.gym_weight = request.POST['gym_weight']
        else:
            return redirect("/dashboard")



        if len(str(request.POST['puls'])) > 0 and test_integer(request.POST['puls']):
            WorkOut.puls = int(request.POST['puls'])
        if len(str(request.POST['snittpuls'])) > 0 and test_integer(request.POST['snittpuls']) or test_float(request.POST['snittpuls']):
            WorkOut.snittpuls = float(request.POST['snittpuls'])
        if len(str(request.POST['minpuls'])) > 0 and test_integer(request.POST['minpuls']):
            WorkOut.minpuls = int(request.POST['minpuls'])
        if len(str(request.POST['kalorier'])) > 0 and test_integer(request.POST['kalorier']):
            WorkOut.kalorier = int(request.POST['kalorier'])

        WorkOut.workoutFeel = request.POST['feeling']
        WorkOut.workoutStretch = request.POST['stretch']


        tiden = test_time(request.POST['time'])
        if tiden is not None:
            WorkOut.workoutTime = tiden[0]
            WorkOut.workoutSec = tiden[1]

        WorkOut.workoutUser = User.objects.filter(id=request.user.id).get()

        WorkOut.save()
        TotalWorkouts.objects.filter(user_id=request.user.id).get().save()

        return redirect("/dashboard")
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

def test_integer(x):
    try:
        int(x)
        return True
    except ValueError:
        return False

def test_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

def test_string(x):
    return len(x) <= 255

def test_time(x):
    fixed = []
    if ":" in str(x):
        s = x.split(":")
        if len(s) > 2:
            return None

        for d in s:
            if d.isdigit():
                fixed.append(int(d))
            else:
                fixed.append(0)

        return fixed

    elif test_integer(x):
        return [int(x),0]

    else:
        return [0,0]

