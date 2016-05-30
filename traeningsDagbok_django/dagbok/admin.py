from django.contrib import admin
from . import models


# Register your models here.

class WorkOutsAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.WorkOuts, WorkOutsAdmin)
admin.site.register(models.UserExtended)
admin.site.register(models.TotalWorkouts)
admin.site.register(models.Goals)
#~ admin.site.register(models.GymWorkout)
