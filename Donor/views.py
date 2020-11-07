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

# Create your views here.

# Cairo = (30.06263, 31.24967)
# Mansoura = (31.03637, 31.38069)
# Alexandria = (31.20176, 29.91582)
# AlMahallah = (30.97063, 31.1669)
# Aswan = (24.09082, 32.89942)
# Luxor = (25.69893, 32.6421)
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
    context=""
    if request.method == 'POST':
        city = request.POST['city']
        bloodtype = request.POST['bloodtype']
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
            print(datetime.now().date())
            # context=whoCanDonate(city,bloodtype)
            # context=donorsDataHaveSameBloodType(bloodtype)
            donation=donorsDataHaveSameBloodType(bloodtype)
            evaluation(donation,citiess['Cairo'])

        else:
            print(request.POST)
            print(form.errors)
    
    form = HospitalForm()
    return render(request, "Donor/hospital.html", {'form': form,'context':context})


def whoCanDonate(city,bloodtype):
    if not Donor.objects.filter(city=city,bloodtype=bloodtype).exists():
        return ("No one at this city")
    else :
        donor = Donor.objects.filter(city=city,bloodtype=bloodtype)
        names = [c.name for c in Donor.objects.filter(city=city,bloodtype=bloodtype)]
        mails = [c.email for c in Donor.objects.filter(city=city,bloodtype=bloodtype)]
        bloodtypes = [c.bloodtype for c in Donor.objects.filter(city=city,bloodtype=bloodtype)]
        cities = [c.city for c in Donor.objects.filter(city=city,bloodtype=bloodtype)]
        res = "\n".join("{} his mail is {} his blood type {} from {}".format(a,b,x, y) for a, b ,x ,y in zip(names, mails , bloodtypes,cities))
        return res
        

def distance(city1,city2):
      
    return (geodesic(city1, city2).km) 


def donorsDataHaveSameBloodType(bloodtype):
    today = datetime.now().date()
    if not Donor.objects.filter(bloodtype=bloodtype).exists():
        return ("No one has this Blood type")
    else :
        donor = Donor.objects.filter(bloodtype=bloodtype ,available="1" , BloodExpirationDate__gte= today)
        # names = [c.name for c in Donor.objects.filter(bloodtype=bloodtype ,available="1" , BloodExpirationDate__gte= today)]
        # bloodtypes = [c.bloodtype for c in Donor.objects.filter(bloodtype=bloodtype ,available="1" , BloodExpirationDate__gte= today)]
        # cities = [c.city for c in Donor.objects.filter(bloodtype=bloodtype ,available="1" , BloodExpirationDate__gte= today)]
        # res = "\n".join("{}  his blood type {} from {}".format(a,b,x) for a, b ,x  in zip(names, bloodtypes,cities))
        return (donor)
    
def evaluation (donations,mainCity):
    sum = 0 
    for i in donations:
        cityy = i.city
        dis = distance(mainCity,citiess[cityy])
        print(dis)
        sum += dis
    print(sum)
    