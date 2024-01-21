from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from blog.models import *
from . models import *
import openpyxl



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created. You can now login!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

@login_required
def profile(request):

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        try:
            if u_form.is_valid and p_form.is_valid:
                u_form.save()
                p_form.save()
                messages.success(
                    request, f"Your account has been successfully Updated!")
                return redirect("profile")
        except Exception as e:
            messages.warning(request, f"{e}")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "users/profile.html", context)

@login_required
def follow_user(request, *args, **kwargs):
    id = request.POST.get('post_author_profile_id')
    profile = Profile.objects.get(id=id)
    profile.followed_by.add(request.user.profile)
    profile.save()
    return redirect('blog-home')

@login_required
def unfollow_user(request, *args, **kwargs):
    id = request.POST.get('post_author_profile_id')
    profile = Profile.objects.get(id=id)
    profile.followed_by.remove(request.user.profile)
    profile.save()
    return redirect('blog-home')

@login_required
def my_feed(request):
    posts = Post.objects.all()
    profiles = request.user.profile.follows.all()
    context = {
        'posts':posts,
        'profiles':profiles
    }
    return render(request, 'users/my_feed.html', context) 