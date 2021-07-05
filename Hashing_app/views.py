from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import forms
from django.contrib.auth import authenticate,login,logout
from .models import UserProfileInfo
from .forms import UserForm, UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def dear(request):
    return render(request,'index.html')

@login_required()
def special(request):
    return HttpResponse("You are logged in, Nice!")


@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def dumb(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/')

            else:
                return HttpResponse("ACCOUNT IS NOT ACTIVE")

        else:
            print("Someone tried to Login and Failed!")
            print("username: {} and password {}".format(username,password))
            return HttpResponse("invalid login details supplied!")
    return render(request,'login.html')


def drop(request):
    registered = False
    user_form = forms.UserForm()
    profile_form = forms.UserProfileInfoForm()
    if request.method == "POST":
        user_form = forms.UserForm(data=request.POST)
        profile_form = forms.UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'registration.html',
                  {'user_form':user_form,'profile_form':profile_form,'registered':registered})
