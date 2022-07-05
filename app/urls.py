from email.mime import base
from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


# router = DefaultRouter()
# router.register('users', views.UserViewSet)
# router.register('register', views.RegisterAPIView(), basename='register')

urlpatterns = [
    # path('api/', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register', views.RegisterAPIView.as_view(), name='register'),
    
]