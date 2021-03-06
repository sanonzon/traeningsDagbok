# coding=utf-8

"""traeningsDagbok_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from dagbok import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^calendar/$', views.calendar, name='calendar'),
    url(r'^profile/$', views.profile, name='profile'),
    #~ url(r'^user/(?P<variabel>[a-z]+)$', views.profile, name='profile'),
    url(r'^user/', views.user, name='user'),
    url(r'^goals/', views.goals, name='goals'),
    url(r'^progress/', views.progress, name='progress'),
    url(r'^settings/', views.settings, name='settings'),
    url(r'^searched/$', views.searched, name='searched'),
    url(r'^admin/', admin.site.urls),
    url(r'^dagbok/', include('dagbok.urls')),
    url(r'^update_user/$', views.update_user, name='update_user'),
    url(r'^advanced_workout$', views.advanced_workout, name='advanced_workout'),
    url(r'^add_buddy$', views.add_buddy, name='add_buddy'),
    url(r'^forum/', include('forum.urls'), name='forum'),
    url(r'^delete_workout$', views.delete_workout, name='delete_workout'),
    url(r'^change_workout/([\d]+)$', views.change_workout, name='change_workout'),
    url(r'^update_workout$', views.update_workout, name='update_workout'),
    url(r'^alerts/', views.update_alerts, name='alerts'),
    url(r'^fbshr/workout/([\d]+)$', views.facebook_share),
    
]
