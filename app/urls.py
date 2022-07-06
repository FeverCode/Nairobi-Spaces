from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from app.views import VerifyEmail, RegisterView


urlpatterns = [
    # path('user', views.AuthUserAPIView.as_view(), name='user'),
    path('register/',RegisterView.as_view(), name='register'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('user/', views.UserView.as_view(), name='user'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    
]