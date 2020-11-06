from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.http import HttpResponseRedirect
from registration.models import User
from .forms import UserForm
from django.core.exceptions import ValidationError

from django.urls import reverse
from django.shortcuts import redirect


def signup(request):
    if request.method == 'POST':

        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login')
        else:
            print(request.POST)
            print(form.errors)
    form = UserForm()
    return render(request, 'registration/signup.html', {'form': form})


# def login(request):
#     return render(request, 'registration/login.html')


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)
        if user is not None:
            print("You are Logged in") 
            return redirect(reverse('/register'))

        else:
            print("Please Enter Valid Email or Password")
            messages.error(request, 'Please Enter Valid Email or Password')
            # return HttpResponseRedirect('/login')
    return render(request,'registration/login.html')


def authenticate(email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email,password=password)
        except User.DoesNotExist:
            return None
        else:
            return user
            

# def authenticate(email, password):
#     users = User.objects.all()
#     if email not in users.email :
#         return "email not valid"
#     elif 
#     else :
#         donor = Donor.objects.filter(city=city,bloodtype=bloodtype)
#         names = [c.name for c in Donor.objects.filter(city=city,bloodtype=bloodtype)]
#         mails = [c.email for c in Donor.objects.filter(city=city,bloodtype=bloodtype)]
#         bloodtypes = [c.bloodtype for c in Donor.objects.filter(city=city,bloodtype=bloodtype)]
#         cities = [c.city for c in Donor.objects.filter(city=city,bloodtype=bloodtype)]
#         res = "\n".join("{} his mail is {} his blood type {} from {}".format(a,b,x, y) for a, b ,x ,y in zip(names, mails , bloodtypes,cities))
#         return res
        