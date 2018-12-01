from django.db import models
import uuid #creates unique istance for the event prenotation
from django.contrib.auth.models import User
from datetime import date

# Django rest authentication includes

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# List Import

from jsonfield import JSONField

class Event(models.Model):
    name = models.CharField(max_length=200, default='name')
    crowd_pic = models.ImageField(upload_to = 'reservations/static', default = 'pic_folder/None/no-img.jpg')
    description = models.CharField(max_length=200, default='name')
    dates = JSONField(blank=True, null=True)
    subsStart = models.CharField(max_length=200, default='', blank=True, null=True)
    contDeadline = models.CharField(max_length=200, default='', blank=True, null=True)
    subsDeadline = models.CharField(max_length=200, default='', blank=True, null=True)
    nation = models.CharField(max_length=200, default='nation')
    city = models.CharField(max_length=200, default='city')
    address = models.CharField(max_length=200, default='address')
    cap = models.CharField(max_length=200, default='cap')
    location = models.CharField(max_length=200, default='location')
    max_seats = models.IntegerField(default=0)
    available_seats = models.IntegerField(default=0)
    date = models.DateTimeField('date published', auto_now=True)
    ticket_price = models.FloatField(default=0)
    staff_ticket_price = models.FloatField(default=0)
    available_money = models.FloatField(default=0)
    is_open = models.BooleanField(default=False)
    is_open_contr = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        #equipara max seats a available seats solo se l'evento è in fase di creazione
        if self.pk is None:
            self.available_seats = self.max_seats
        super(Event, self).save(*args, **kwargs)



class EventReservation(models.Model):
    event = models.IntegerField(default=0)
    user = models.IntegerField(default=0)
    is_staff = models.BooleanField(default=False)
    bank_user = models.CharField(max_length=255, default='')

class Document(models.Model):
    name = models.CharField(max_length=255)
    document = models.FileField(upload_to='documents/')
    reservation = models.CharField(max_length=200, default='reservation')

class Like(models.Model):
    owner = models.ForeignKey(User, related_name='like_user_set', on_delete=models.SET_NULL, null=True)
    pref_link = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)

class Wallet(models.Model):
    accountholder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    public_key = models.CharField(max_length=255)

class ArtistContracts(models.Model):
    artist = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    likoin_address = models.CharField(max_length=255, default='')
    buck_address = models.CharField(max_length=255, default='')
    crowdsale_address = models.CharField(max_length=255, default='')

# This code is triggered whenever a new user has been created and saved to the database

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
