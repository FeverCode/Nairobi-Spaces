from django.shortcuts import get_object_or_404, render
from rest_framework import response, generics, status, views, permissions,viewsets
from app.models import Profile, Reservation, Spaces, User
from app.renderers import UserRenderer
from app.serializers import LoginSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, SpacesSerializer, UserSerializer, RegisterSerializer, EmailVerificationSerializer, GoogleSocialAuthSerializer, ProfileSerializer, ReservationSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from rest_framework.views import APIView
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from .permissions import (IsOwnerOrReadOnly, IsAdminUserOrReadOnly, IsSameUserAllowEditionOrReadOnly)


# Create your views here.

class RegisterView(generics.GenericAPIView):
    
    """User registers with name, email and password

    Returns:
        sends verification email with activation token
    """    
   
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)
    
    
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)
        
       
    
    
class VerifyEmail(views.APIView):
    
    """Email verification view

    """    
    
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms='HS256')
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
            
        
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
    
class UserList(generics.ListCreateAPIView):
    
    """Creates a user instance view

    Raises:
        AuthenticationFailed: when wrong password is entered
        AuthenticationFailed: when email is not verified

    Returns:
        verified user details
    """    
    
    
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsSameUserAllowEditionOrReadOnly,)
    
    
    def post (self, request,format=None):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def get(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('unauthorized')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer_context = {
            'request': request,
        }
        serializer = UserSerializer(user, context=serializer_context)
        return Response(serializer.data)
    
    
class ProfileAPI(RetrieveUpdateDestroyAPIView):
    """_summary_ = 'Update a user profile'

    Args:
        RetrieveUpdateDestroyAPIView (_type_): updates a user profile, displays a user profile, deletes a user profile

    Returns:
        _type_: _description_
    """    
    
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    queryset = Profile.objects.all()
    lookup_field = 'id'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    

    
    
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)

        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret',
                           algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


    
class LogoutView(APIView):
    
    def post(self, request):
        response= Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'logged out'
        }
        
        return response 
     
        
class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
    

class PasswordTokenCheckAPI(generics.GenericAPIView):
      serializer_class = SetNewPasswordSerializer
      
      def get(self,request,uidb64,token):
          
          
          try:
              id = smart_str(urlsafe_base64_decode(uidb64))
              user=User.objects.get(id=id)
              
              if not PasswordResetTokenGenerator().check_token(user,token):
                  return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
              
              return Response({'success':True,'message':'Credentials Valid', 'uidb64':uidb64,'token':token},status=status.HTTP_200_OK)
              
              
                   
          except DjangoUnicodeDecodeError as identifier:
              if not PasswordResetTokenGenerator():
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
    


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class=SetNewPasswordSerializer
    
    def patch(self,request):
        serializer =self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True,'message':'Password reset success'},status=status.HTTP_200_OK)

class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an idtoken as from google to get user information
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)

    
class ReservationListAPIView(ListCreateAPIView):
    
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    


class ReservationDetailAPIView(RetrieveUpdateDestroyAPIView):
    
    serializer_class = ReservationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Reservation.objects.all()
    lookup_field = 'id'
    
    def post(self, request, format=None):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class SpacesListAPIView(ListCreateAPIView):

    serializer_class = SpacesSerializer
    queryset = Spaces.objects.all()
