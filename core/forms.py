from django import forms
from .models import Reservation, Guest
from core.models import WebsiteUser
from django.contrib.auth.hashers import make_password

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['name', 'email', 'phone']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['check_in', 'check_out']  # no 'room' here

class WebsiteUserRegisterForm(forms.ModelForm):
    class Meta:
        model = WebsiteUser
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'id': 'reg_username'}),
            'email': forms.EmailInput(attrs={'id': 'reg_email'}),
            'password': forms.PasswordInput(attrs={'id': 'reg_password'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
class WebsiteUserLoginForm(forms.Form):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs={'id': 'login_username'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'id': 'login_password'}))

    
    from django import forms
from core.models import Product, ProductOrder

from django import forms
from .models import ContactMessage

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'placeholder': 'Message...', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'placeholder': 'Your Name*', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email*', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your Phone*', 'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import RoomServiceRequest

class RoomServiceRequestForm(forms.ModelForm):
    class Meta:
        model = RoomServiceRequest
        fields = ['guest', 'room', 'service_type', 'fulfilled']

