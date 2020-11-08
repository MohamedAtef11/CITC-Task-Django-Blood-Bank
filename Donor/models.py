from django.db import models
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator
from datetime import datetime  
from datetime import timedelta  
from django.contrib.auth.models import User 

# Create your models here.


class Donor(models.Model):
    nationalID = models.CharField(max_length=14 ) 
    name = models.CharField(max_length=50 ,null=True,  verbose_name=("Name")) 
    city= models.CharField(max_length=30 ,null=True  )
    email = models.EmailField(max_length=50) 
    virustest = models.CharField(max_length=60)
    bloodtype = models.CharField(max_length=60)
    BloodExpirationDate =  models.DateField(default=(datetime.now() + timedelta(days=42)))  
    created_at = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True , null=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE )

    # def __str__(self):
    #     return self.name

class Hospital(models.Model):
    bloodtype = models.CharField(max_length=60)
    city= models.CharField(max_length=30 ,null=True  )
    patientsStatus = models.CharField(max_length=50 ,null=True) 
    bloodQuantity = models.IntegerField(default=1)