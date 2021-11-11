from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class NationalForm(forms.ModelForm):

    class Meta:
        model = NationalId
        fields = ('firstname', 'name', 'famName', 'address', 'dateofbirth', 'phone', 'fathername', 'mothername')


class HealthForm(forms.ModelForm):
    
    class Meta:
        model = HealthReport
        fields = '__all__'
    
    

class CardForm(forms.ModelForm):
    
    class Meta:
        model = Card
        fields = ('cardnum', 'status')

class AccountForm(UserCreationForm):
    
    class Meta:
        model = PersonnalizedAccount
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')
        
class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = '__all__'
      
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        existing = Card.objects.filter(status='pending')
        self.fields['cardNum'].queryset = existing

class EditProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('typeUser', 'cardNum')

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        existing = Card.objects.filter(status='pending')
        self.fields['cardNum'].queryset = existing

class AssignForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ('account', 'health', 'cardNum')
    def __init__(self, *args, **kwargs):
        super(AssignForm, self).__init__(*args, **kwargs)
        existing = Card.objects.filter(status='pending')
        self.fields['cardNum'].queryset = existing

class CashForm(forms.ModelForm):
    
    class Meta:
        model = Cash
        fields = ('account', 'balance')



class RoadForm(forms.ModelForm):
    
    class Meta:
        model = Road
        fields = '__all__'

class BusStationForm(forms.ModelForm):
    
    class Meta:
        model = BusStation
        fields = '__all__'

class BusForm(forms.ModelForm):
    
    class Meta:
        model = Bus
        fields = '__all__'
    

    def __init__(self, *args, **kwargs):
        super(BusForm, self).__init__(*args, **kwargs)
        existing = Profile.objects.filter(typeUser='Driver')
        self.fields['affectDriver'].queryset = existing