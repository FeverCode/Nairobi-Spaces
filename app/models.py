from re import sub
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from cloudinary.models import CloudinaryField
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


# Create your models here.

class Spaces(models.Model):
    CHOICE = (
        ('Suncity Picnic Scene', 'Suncity Picnic Scene'),
        ('Serenity Chill Space', 'Serenity Chill Space'),
        ('Ihub Office Workspace', 'Ihub Office Workspace'),
    )
    name = models.CharField(max_length=200, choices=CHOICE, blank=True)
    description = models.TextField()
    photo = CloudinaryField('Image')
    price = models.DecimalField(max_digits=20, decimal_places=2)
    location = models.CharField(max_length=255)
    
    class Meta:
        ordering = ['-id']
    

    def __str__(self):
        return self.name

    def create_Spaces(self):
        self.save()

    def delete_Spaces(self):
        self.delete()

    def update_Spaces(self, new_choice):
        self.space = new_choice
        self.save()

    @classmethod
    def search_by_name(cls, search_term):
        space = cls.objects.filter(name=search_term)
        return space
    
    @classmethod
    def search_by_location(cls, search_term):
        location = cls.objects.filter(location=search_term)
        return location

    @classmethod
    def search_by_price(cls, search_term):
        price = cls.objects.filter(price=search_term)
        return price

class Reservation(models.Model):
    space = models.ForeignKey(Spaces, on_delete=models.CASCADE, related_name='space')
    numberOfPeople = models.IntegerField()
    owner = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE)
    dateFrom = models.DateField(null=False, blank=False, unique=True)
    dateTo = models.DateField(null=False, blank=False, unique=True)
    time = models.TimeField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.owner)+'s reservations'

    def create_reservation(self):
        self.save()

    def delete_reservation(self):
        self.delete()

    def update_reservation(self, new_space):
        self.name = new_space
        self.save()


class Reviews(models.Model):
    review = models.TextField(max_length=500)
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.review)

    def create_review(self):
        self.save()
        
    def delete_review(self):
        self.delete()
        
    def update_review(self, review):
        self.review = review
        self.save()
        
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    photo = CloudinaryField('image', default='https://res.cloudinary.com/fevercode/image/upload/v1654534329/default_n0r7rf.png')
    username = models.CharField(max_length=255, blank=True)
    phone_regex = RegexValidator(regex='^[0-9]{10}$', message="Phone number must field up to 10 digits allowed.")
    contact = models.CharField(validators=[phone_regex], max_length=13, blank=True)  # Validators should be a list
    location = models.CharField(max_length=255)
    bio = models.TextField(max_length=500, default='This is my bio')
    reviews = models.ForeignKey(Reviews, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
    
    
class SubscribedUsers(models.Model):
    email = models.EmailField()
