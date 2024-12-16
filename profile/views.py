from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import Profile
from django.contrib.auth.models import User
from .forms import ProfileForm


@login_required
def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    posts = user.blog_posts.all()

    context = { 
        'profile': profile,
        'posts': posts,
        }
    return render(request, "profile/profile_detail.html", context)


@login_required
def profile_setup(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Profile updated successfully!"})
        else:
            return JsonResponse({"errors": form.errors}, status=400)

    form = ProfileForm(instance=profile)
    return render(request, "profiles/profile_setup.html", {"form": form, "profile": profile})


@login_required
def edit_profile(request):
    profile = request.user.profile  
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile_detail", username=request.user.username)  
    else:
        form = ProfileForm(instance=profile)  
    return render(request, "profile/edit_profile.html", {"form": form, "profile": profile})


@login_required
def delete_profile(request):
    user = request.user
    if request.method == "POST":
        user.delete()
        logout(request)  
        return redirect("home")  
    return render(request, "profile/delete_profile.html")

