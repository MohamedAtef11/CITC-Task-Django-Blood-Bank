from django import forms
from .models import Donor , Hospital


class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['nationalID', 'name', 'city','email','virustest','bloodtype']


class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['bloodtype', 'city', 'patientsStatus','bloodQuantity']