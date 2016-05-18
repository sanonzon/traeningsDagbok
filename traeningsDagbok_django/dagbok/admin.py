from django.contrib import admin
from . import models


# Register your models here.

class Workout_gymAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Workout_gym, Workout_gymAdmin)

class SwimmingAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Swimming, SwimmingAdmin)

class WorkOutsAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.WorkOuts, WorkOutsAdmin)
