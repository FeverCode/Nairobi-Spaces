
from django.shortcuts import render
from rest_framework import response
from rest_framework import generics, status, views, permissions
from app.serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.generics import GenericAPIView


# Create your views here.


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
#     def post(self, request):
#         user = request.data
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         user_data = serializer.data
#         user=User.objects.get(email=user_data['email'])
        
#         token=RefreshToken.for_user(user).access_token
        
#         current_site=get_current_site(request).domain
#         relativeLink=reverse('verify-email')
#         absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
#         email_body = 'Hi '+user.username + \
#             ' Use the link below to verify your email \n' + absurl
#         data = {'email_body': email_body, 'to_email': user.email,
#                 'email_subject': 'Verify your email'}
#         Util.send_email(data)
        
        
# class VerifyEmailViewSet(viewsets.ModelViewSet):
#     def get(self):
#         pass
        
        
        
        
    
    
class RegisterAPIView(GenericAPIView):

    serializer_class = RegisterSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
    
    
    


#     def post(self, request):
#         user = request.data
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         user_data = serializer.data
#         user = User.objects.get(email=user_data['email'])
#         token = RefreshToken.for_user(user).access_token
#         current_site = get_current_site(request).domain
#         relativeLink = reverse('email-verify')
#         absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
#         email_body = 'Hi '+user.username + \
#             ' Use the link below to verify your email \n' + absurl
#         data = {'email_body': email_body, 'to_email': user.email,
#                 'email_subject': 'Verify your email'}

#         Util.send_email(data)
#         return Response(user_data, status=status.HTTP_201_CREATED)
    
#     def post (self, request):
#         user = request.data
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         user_data = serializer.data
#         user = User.objects.get(email=user_data['email'])
        
#         token = RefreshToken.for_user(user)
        
#         current_site = get_current_site(request)
#         relativeLink=''
#         data={'domain':current_site.delete}
        
#         Util.send_email(data)
        
#         return Response(user_data, status=status.HTTP_201_CREATED)

# class VerifyEmail(generics.GenericAPIView):
#     def get (self):
#         pass