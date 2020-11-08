from django.shortcuts import render
from django.contrib.auth.forms import  UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from geopy.distance import geodesic 
from datetime import datetime  
from datetime import timedelta  
from .forms import DonorForm ,HospitalForm
from .models import Donor , Hospital
from datetime import datetime
from .mail import send_email 
import  numpy as np
from geneticalgorithm import geneticalgorithm as ga

# Create your views here.

citiess = {'Cairo': (30.06263, 31.24967), 'mansoura': (31.03637, 31.38069) ,
            'Alexandria':(31.20176, 29.91582) ,'AlMahallah' : (30.97063, 31.1669),
            'Aswan' : (24.09082, 32.89942),'Luxor' :(25.69893, 32.6421)} 
@login_required(login_url='/login/')
def donate(request):
    print (distance(citiess["Cairo"],citiess["mansoura"]))
    if request.method == 'POST':
        nationalID = request.POST['nationalID']
        virustest = request.POST['virustest']
        email=request.POST['email']
        if canDonate(nationalID) and virustest=="Negative" :
            form = DonorForm(request.POST)
            if form.is_valid():
                form.instance.id_user_id=request.session['logged_in_user']
                form.save()
                send_email(email,
                            'Blood Bank',
                            'Congratulations! you can donate ')
                return HttpResponseRedirect('#')
            else:
                print(request.POST)
                print(form.errors)
        else:
            print(virustest)
            print(email)
            if not canDonate(nationalID) and virustest=="Positive" :
                send_email(email,
                                'Blood Bank',
                                'Sorry, you can not donate because your virustest is "Positive" and you must donate after three months from your last donation')
            elif virustest=="Positive" :
                send_email(email,
                                'Blood Bank',
                                'Sorry, you can not donate because your virustest is "Positive"')
            else:
                send_email(email,
                                'Blood Bank',
                                'Sorry, you can not donate because you must donate after three months from your last donation ')
    form = DonorForm()
    return render(request, "Donor/donate.html", {'form': form})


def canDonate(nationalid):
    if not Donor.objects.filter(nationalID=nationalid).exists():
        return True
    else:
        donor = Donor.objects.filter(nationalID=nationalid).order_by('-created_at')[0]
        delta = datetime.now().date() - donor.created_at.date()
        if delta.days <= 90 :
            return False
        else:
            return True


def hospital(request):
    header = ['Name', 'City','Blood Type' , 'Donate at' ,'Expired at', 'available']
    context=""
    error=""
    len_data=0
    len_error=0
    arr_donors=[]
    if request.method == 'POST':
        city = request.POST['city']
        bloodtype = request.POST['bloodtype']
        patientsStatus = request.POST['patientsStatus']
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
            allDonations=donorsDataHaveSameBloodType(bloodtype)
            iteration=1
            if patientsStatus == "Normal":
                iteration=2
            elif patientsStatus == "Immediate":
                iteration=5
            else:
                iteration=30
            if allDonations == "No one has this Blood type":
                error="No one have this blood type"
                len_error=len(error)
            else:
                donors_ga = eval_min(citiess[city],allDonations,iteration)
                for i in set(donors_ga['variable']):
                    arr_donors.append(allDonations[int(i)])
                len_data=(len(arr_donors))
            

        else:
            print(request.POST)
            print(form.errors)
    
    form = HospitalForm()
    return render(request, "Donor/hospital.html", {'form': form,'arr_donors':arr_donors , 'header':header,'len_data':len_data,'len_error':len_error})


def distance(city1,city2):
      
    return (geodesic(city1, city2).km) 


def donorsDataHaveSameBloodType(bloodtype):
    today = datetime.now().date()
    if not Donor.objects.filter(bloodtype=bloodtype).exists():
        return ("No one has this Blood type")
    else :
        donor = Donor.objects.filter(bloodtype=bloodtype ,available="1" , BloodExpirationDate__gte= today)
        return (donor)
    
def evaluation (donations,mainCity):
    sum = 0 
    for i in donations:
        cityy = i.city
        dis = distance(mainCity,citiess[cityy])
        sum += dis
    return (sum)
    
def eval_min(maincity,allDonations,iteration):
    def f(X):
        xx = convert_index_to_object (X,allDonations)
        yy = evaluation(xx,maincity)
        return yy
    varbound=np.array([[0,len(allDonations)-1]]*10)
    algorithm_param = {'max_num_iteration': 10*iteration,\
                   'population_size':10,\
                   'mutation_probability':0.1,\
                   'elit_ratio': 0.01,\
                   'crossover_probability': 0.5,\
                   'parents_portion': 0.3,\
                   'crossover_type':'uniform',\
                   'max_iteration_without_improv':None}
    model=ga(function=f,dimension=10,variable_type='int',variable_boundaries=varbound , algorithm_parameters=algorithm_param)
    model.run()
    return model.output_dict
  
def convert_index_to_object (arr,allDonations):
    new_arr=[]
    for i in arr :
        i = int(i)
        new_arr.append(allDonations[i])
    return new_arr