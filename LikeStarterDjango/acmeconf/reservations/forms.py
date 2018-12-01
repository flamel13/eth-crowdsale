from django.contrib.auth.models import User
from django import forms
from .models import EventReservation
from .models import Event
from .models import Document
from .models import Wallet

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    wallet = forms.CharField(label='Wallet', max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'wallet']
        exclude = ()

class EventReservationForm(forms.ModelForm):
    name = forms.CharField(label='Name', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = EventReservation
        fields = ['event' , 'is_staff']
        exclude = ('event',)
        labels = {
            'is_staff': ('Conference Speaker'),
        }
        help_texts = {
            'is_staff': ('Check it if you are a conference speaker'),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('name', 'document', 'reservation')
        exclude = ('reservation',)

class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ('public_key',)
        exclude = ('accountholder',)

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'crowd_pic', 'description',]
        labels = {
            'crowd_pic': ('Image'),
        }
