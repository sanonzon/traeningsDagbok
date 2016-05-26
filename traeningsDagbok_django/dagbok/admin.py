from django.contrib import admin
from . import models


# Register your models here.

class WorkOutsAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.WorkOuts, WorkOutsAdmin)
#~ admin.site.register(models.GymWorkout)
