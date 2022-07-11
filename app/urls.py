from django.urls import path
from . import views
from app.views import PasswordTokenCheckAPI, ProfileAPI, RequestPasswordResetEmail, ReservationDetailAPIView, ReservationListAPIView, SetNewPasswordAPIView, SpacesListAPIView, VerifyEmail, RegisterView, GoogleSocialAuthView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/',RegisterView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('login/', views.LoginView.as_view(), name='login'),
    path('user/', views.UserList.as_view(), name='user'),
    path('user/<int:id>/profile/', ProfileAPI.as_view()),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('request-reset-password', RequestPasswordResetEmail.as_view(),name='request-reset-password'),
    path('password-reset/<uidb64>/<token>/',PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    path('google/', GoogleSocialAuthView.as_view()),
    path('reservations/', ReservationListAPIView.as_view(), name='reservations'),
    path('reservations/<int:id>', views.ReservationDetailAPIView.as_view(),name='reservations'),
    path('spaces/', SpacesListAPIView.as_view(), name='spaces'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
