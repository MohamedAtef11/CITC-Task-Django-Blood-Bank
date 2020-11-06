from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=50 ,null=True,  verbose_name=("Name")) 
    email = models.EmailField(max_length=50) 
    city= models.CharField(max_length=30 ,null=True  )
    password = models.CharField(max_length=255)
