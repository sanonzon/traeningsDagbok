#coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.core.urlresolvers import reverse

from .forms import PostForm, CommentForm
from .models import Post, Comment, Category

# Create your views here.

def index(request):
    if request.user.is_authenticated():
        c = Category.choices
        fixed_list = [l[0] for l in c]
        
        return render(request, "forum/index.html", {'category':fixed_list})
    else:
        return redirect("/")
def category(request, category):
    if request.user.is_authenticated():
        pf = PostForm()
        p = Post.objects.filter(category=category)
        
        return render(request, "forum/category.html", {'category':category,'posts':p,'form':pf})
    else:
        return redirect("/")
def post(request, post):
    if request.user.is_authenticated():
        p = Post.objects.filter(id=post)
        c = Comment.objects.filter(postParent=post)
        cf = CommentForm()
        
        return render(request, "forum/post.html", {'post_id':post, 'post':p, 'form':cf, 'comments':c, 'category':p.get().category})
    else:
        return redirect("/")
    
def new_post(request):
    if request.user.is_authenticated():
        p = Post()
        p.title = request.POST['title']
        p.text = request.POST['text']
        p.category = request.POST['category']
        p.author = User.objects.filter(id=request.user.id).get()
        
        p.save()
        return redirect("/forum/")
    else:
        return redirect("/")
def new_comment(request):
    if request.user.is_authenticated():        
        c = Comment()
        c.text = request.POST['text']
        c.postParent = Post.objects.filter(id=request.POST['parent']).get()    
        c.author = User.objects.filter(id=request.user.id).get()
        
        c.save()
        return redirect("/forum/post/"+request.POST['parent'])
    else:
        return redirect("/")
