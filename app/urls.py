from django.urls import include, path
from app.forms import LoginForm
from .views import CreateReservationtView, UpdateReservationView, ReservationDeleteView
from rest_framework_simplejwt.views import (TokenRefreshView,)
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegisterView.as_view(), name='users-register'),
    path('login/', views.CustomLoginView.as_view(redirect_authenticated_user=True,template_name='registration/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('profile/', views.profile, name='profile'),
    path('edit/profile/', views.edit_profile, name='edit-profile'),
    path('space/', views.space, name='space'),
    path('<int:pk>/delete', ReservationDeleteView.as_view(),name='delete-reservation'),
    path('reservation/<int:pk>/', UpdateReservationView.as_view(), name='reservation'),
    path('reservation/', CreateReservationtView.as_view(),name='update-reservation'),
    path('newsletter/', views.newsletter, name='newsletter'),
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # path('register/',RegisterAPIView.as_view(), name='register'),
    # path('login/', views.LoginAPIView.as_view(), name='login'),
    # path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('login/', views.LoginView.as_view(), name='login'),
    # path('user/', views.UserList.as_view(), name='user'),
    # path('user/<int:pk>/', views.UserDetail.as_view()),
    # path('user/profile/', views.ProfileList.as_view()),
    # path('user/<int:pk>/', views.UserDetail.as_view()),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('request-reset-password', RequestPasswordResetEmail.as_view(),name='request-reset-password'),
    # path('password-reset/<uidb64>/<token>/',PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    # path('password-reset-complete', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    # path('google/', GoogleSocialAuthView.as_view()),
    # path('reservations/', views.ReservationList.as_view(), name='reservations'),
    # path('reservations/<int:id>/',views.ReservationDetail.as_view(), name='reservations'),
    # path('spaces/', SpacesListAPIView.as_view(), name='spaces'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
