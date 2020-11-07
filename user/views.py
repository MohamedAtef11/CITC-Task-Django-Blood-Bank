from django.shortcuts import render, redirect 
from django.contrib import messages 
from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import AuthenticationForm 
from .forms import UserRegisterForm 
from django.core.mail import send_mail 
from django.core.mail import EmailMultiAlternatives 
from django.template.loader import get_template 
from django.template import Context 
from django.contrib.auth.models import User 
from django.views.decorators.csrf import ensure_csrf_cookie
from Donor.models import Donor 

def index(request): 
    context={}
    try:
        user = User.objects.get(id=request.session['logged_in_user'])
        id_user = user.id
        donor_data = Donor.objects.filter(id_user=id_user)
        header = ['Name', 'City','Blood Type' , 'Donate at' ,'Expired at', 'available']
        len_data=(len(donor_data))
        context = {'username':user , 'header':header ,'donor_data':donor_data , 'len_data':len_data }
    except:
        pass
    return render(request, 'user/index.html',context) 
   
def register(request): 
    if request.method == 'POST': 
        form = UserRegisterForm(request.POST) 
        if form.is_valid(): 
            form.save() 
            username = form.cleaned_data.get('username') 
            email = form.cleaned_data.get('email') 
            return redirect('login') 
    else: 
        form = UserRegisterForm() 
    return render(request, 'user/register.html', {'form': form}) 

@ensure_csrf_cookie
def Login(request): 
    
    if request.method == 'POST': 
   
        username = request.POST['username'] 
        password = request.POST['password'] 
        user = authenticate(request, username = username, password = password) 
        if user is not None: 
            form = login(request, user) 
            logged_user = User.objects.get(username=username).pk
            # User.objects.get(username = username, password = password)
            request.session['logged_in_user'] = logged_user
            return redirect('index') 
        else: 
            messages.info(request, f'account dose not exist please sign up') 
    form = AuthenticationForm() 
    return render(request, 'user/login.html', {'form':form}) 