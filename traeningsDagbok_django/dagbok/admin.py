from django.contrib import admin
from .models import users
from .models import workout_type
from .models import workout_gym


# Register your models here.
class usersAdmin(admin.ModelAdmin):
    fields = ['username', 'password']
    

class workout_gymAdmin(admin.ModelAdmin):
    fields = ['gym_type']
    
admin.site.register(users, usersAdmin)
admin.site.register(workout_gym, workout_gymAdmin)
