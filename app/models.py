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


# AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google',
#                   'twitter': 'twitter', 'email': 'email'}


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # auth_provider = models.CharField(
    #     max_length=255, blank=False,
    #     null=False, default=AUTH_PROVIDERS.get('email'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email
      
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


# class Spaces(models.Model):
#     CHOICE = (
#         ('Suncity Picnic Scene', 'Suncity Picnic Scene'),
#         ('Serenity Chill Space ', 'Serenity Chill Space '),
#         ('Ihub Office Workspace ', 'Ihub Office Workspace'),
#     )
#     name = models.CharField(max_length=200, choices=CHOICE, blank=True)
#     description = models.TextField()
#     photo = CloudinaryField('Image')
#     price = models.DecimalField(max_digits=20, decimal_places=2)
#     location = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name

#     def create_Spaces(self):
#         self.save()

#     def delete_Spaces(self):
#         self.delete()

#     def update_Spaces(self, new_choice):
#         self.deal = new_choice
#         self.save()

#     @classmethod
#     def search_by_name(cls, search_term):
#         space = cls.objects.filter(name=search_term)
#         return space
    
#     @classmethod
#     def search_by_location(cls, search_term):
#         location = cls.objects.filter(location=search_term)
#         return location

#     @classmethod
#     def search_by_price(cls, search_term):
#         price = cls.objects.filter(price=search_term)
#         return price
