from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from . forms import *
from django.http import *

def home(reqest):
    context = {
        'posts': Post.objects.all().order_by('-date_posted')
    }
    return render(reqest, 'blog/home.html', context)

@login_required
def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post(title=title, content=content, author= request.user)
        post.save()
        return redirect('blog-home')
    else:
        form =  create_post_form()
    return render(request, 'blog/post_create.html', {'form':form})     

@login_required
def post_update(request, *args, **kwargs):
    post = Post.objects.get(id=kwargs['pk'])
    if request.user == post.author:
        if request.method == 'POST':
            post.title = request.POST.get('title')
            post.content = request.POST.get('content')
            post.save()
            return redirect('blog-home')
        else:
            form = update_post_form({
                'title': post.title,
                'content': post.content
            })    
    else:
        return HttpResponse('''you cannot update someone else's post ''')
    return render(request, 'blog/post_update.html', {'form':form})          

@login_required
def post_delete(request, *args, **kwargs):
    post = Post.objects.get(id=kwargs['pk'])

    if request.user == post.author:
        if request.method == 'POST':
            post.delete()
            return redirect('blog-home')
    else:
        return HttpResponse('''you cannot delete someone else's post''')
    return render(request, 'blog/post_delete.html', {'post': post})

@login_required 
def post_detail(request, *args, **kwargs):
    form = comment_form()
    posts = Post.objects.filter(id=kwargs['pk'])
    context = {
        'posts': posts,
        'comments': Comment.objects.filter(post=posts.first()),
        'form': form
    }      
    if request.method == 'POST':
        comm = Comment(comment=request.POST.get('comment'),author=request.user, post=posts.first())
        comm.save()  
    else:
        form
    return render(request, 'blog/post_detail.html', context)          

@login_required
def user_posts(request, *args, **kwargs):
    user = User.objects.get(id=kwargs['pk'])
    posts = Post.objects.filter(author = user)
    current_user = request.user
    context = {
        'user': current_user,
        'posts': posts,
        'blog_of_user': user
    }
    return render(request, 'blog/user_posts.html', context)

    