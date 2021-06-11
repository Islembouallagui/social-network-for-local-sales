from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
#from django.forms import ModelForm
from .models import Profile
from .models import Prod
from .models import Service
from django.conf import settings
from django.forms import FloatField
from .models import *
from .models import Review, RATE_CHOICES

class RateForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea'}), required=False)
    rate = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(), required=True)

    class Meta:
        model = Review
        fields = ('text', 'rate')
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    lastname=forms.CharField()
    firstname=forms.CharField()
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2','lastname','firstname']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    last_name=forms.CharField()
    first_name=forms.CharField()
    #Latitude = models.FloatField()
    #Longitude = models.FloatField()
    class Meta:
        model = get_user_model()
        fields = ['username', 'email','last_name','first_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image','phone']

class ServiceRegisterForm(forms.ModelForm):
    image_service = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False, }))
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    class Meta:
        model = Service

        fields = ['name_business','sector','email_business','phone_business','description','disponibilite','Adress','image_service']

class addproduct(forms.ModelForm):
    principal_image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': False, }))
    #image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': False, }))
    Latitude = models.FloatField()
    Longitude = models.FloatField()

    class Meta:
        model = Prod
 
        fields = ['description','disponibilite','prix','Title','quantité','principal_image','Shop','Adress']
  
