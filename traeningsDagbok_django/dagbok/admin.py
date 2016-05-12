from django.contrib import admin
from .models import Workout_type
from .models import Workout_gym


# Register your models here.

class Workout_gymAdmin(admin.ModelAdmin):
    fields = ['gym_type']
    
admin.site.register(Workout_gym, Workout_gymAdmin)
