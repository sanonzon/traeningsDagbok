from django.conf.urls import url

from forum import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^category/([\w]+)$', views.category),
    url(r'^post/([\d]+)$', views.post),
    url(r'^new_post/$', views.new_post),
    url(r'^new_comment/$', views.new_comment),

    #~ url(r'^/$', views.logout_user, name='logout'),
]

