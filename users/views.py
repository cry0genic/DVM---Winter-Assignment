from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
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

#follow user    