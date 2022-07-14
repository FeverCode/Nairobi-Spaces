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



# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


AUTH_PROVIDERS = {'github': 'github', 'google': 'google',
                  'email': 'email'}


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(max_length=255, blank=False,null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email
      
    def tokens(self):
        pass
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class Spaces(models.Model):
    CATEGORY_OPTIONS = (
        ('Suncity Picnic Scene', 'Suncity Picnic Scene'),
        ('Serenity Chill Space', 'Serenity Chill Space'),
        ('Ihub Office Workspace', 'Ihub Office Workspace'),
    )
    name = models.CharField(max_length=200, choices=CATEGORY_OPTIONS, blank=True)
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
        self.deal = new_choice
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
    owner = models.ForeignKey('app.User', related_name='reservations', on_delete=models.CASCADE)
    dateFrom = models.DateField(null=False, blank=False, unique=True)
    dateTo = models.DateField(null=False, blank=False, unique=True)
    time = models.TimeField(null=False, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.user)+'s reservations'

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
    
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()

    def create_profile(self):
        self.save()

    def update_profile(self, new_bio):
        self.bio = new_bio
        self.save()
    


class NewsLetterRecepients(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField()



