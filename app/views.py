from django.shortcuts import get_object_or_404, render,redirect
from django.views import View
from rest_framework import response, generics, status, views, permissions,viewsets
from app.forms import LoginForm, MpesaForm, RegisterForm, ReservationForm, UpdateProfileForm, UpdateUserForm
from app.models import Profile, Reservation, Spaces, SubscribedUsers, User
from app.permissions import IsOwnerOrReadOnly
from app.renderers import UserRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse, reverse_lazy
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
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django_daraja.mpesa.core import MpesaClient
from django.http import HttpResponse, JsonResponse
from decouple import config
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
import re
# Create your views here.
def index(request):
    return render(request, 'index.html')


def space(request):
    return render(request, 'space.html')

def dispatch(self, request, *args, **kwargs):
      # will redirect to the home page if a user tries to access the register page while logged in
       if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
       return super(RegisterView, self).dispatch(request, *args, **kwargs)


class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect('login')

        return render(request, self.template_name, {'form': form})
# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'registration/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('login')


@login_required
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def user_profile(request):
    profile = Profile.objects.all()
    reservations = Reservation.objects.all().order_by('id').reverse()
    return render(request, 'users/profile.html', {'profile': profile, 'reservations': reservations})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(
            request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/edit-profile.html', {'user_form': user_form, 'profile_form': profile_form})


def mpesa_test(request):
    form = MpesaForm(request.POST)

    return render(request, 'pay-test.html', {'form': form})


cl = MpesaClient()
stk_push_callback_url = 'https://mtaani-meetup.herokuapp.com/'
b2c_callback_url = 'https://mtaani-meetup.herokuapp.com/'


def test(request):

    return HttpResponse('Welcome to the home of daraja APIs')


def oauth_success(request):
	r = cl.access_token()
	return JsonResponse(r, safe=False)


def stk_push_success(request):
    if request.method == 'POST':
        form = MpesaForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            amount = form.cleaned_data['amount']
            account_reference = config('TILL_NUMBER')
            transaction_desc = 'STK Push Description'
            callback_url = stk_push_callback_url
            r = cl.stk_push(phone_number, amount,
                            account_reference, transaction_desc, callback_url)
            return JsonResponse(r.response_description, safe=False)

    else:
        return JsonResponse(r.response_description, safe=False)


class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'delete.html'
    success_url = reverse_lazy('profile')


class UpdateReservationView(UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = "reservation.html"
    form_class = ReservationForm
    success_url = reverse_lazy('profile')


class CreateReservationtView(LoginRequiredMixin, CreateView):

    model = Reservation
    form_class = ReservationForm
    template_name = 'reservation.html'
    success_url = reverse_lazy('profile')

    #   ↓        ↓ method of the CreateReservationtView

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    #   ↓              ↓ method of the CreateReservationtView
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'CreateReservationtView'
        return data


def newsletter(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        email = post_data.get("email", None)
        subscribedUsers = SubscribedUsers()
        subscribedUsers.email = email
        subscribedUsers.save()
        # send a confirmation mail
        subject = 'Nairobi Space NewsLetter Subscription'
        message = 'Hello ' + \
            ', Thanks for subscribing us. You will get notification of latest articles posted on our website. Please do not reply on this email.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list)
        res = JsonResponse({'msg': 'Thanks. Subscribed Successfully!'})
        return res
    return render(request, 'index.html')


def validate_email(request):
    email = request.POST.get("email", None)
    if email is None:
        res = JsonResponse({'msg': 'Email is required.'})
    elif SubscribedUsers.objects.get(email=email):
        res = JsonResponse({'msg': 'Email Address already exists'})
    elif not re.match(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", email):
        res = JsonResponse({'msg': 'Invalid Email Address'})
    else:
        res = JsonResponse({'msg': ''})
    return res















# class RegisterView(generics.GenericAPIView):
    
#     """User registers with name, email and password

#     Returns:
#         sends verification email with activation token
#     """    
   
#     serializer_class = RegisterSerializer
#     renderer_classes = (UserRenderer,)
    
    
    
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
        
       
    
    
# class VerifyEmail(views.APIView):
    
#     """Email verification view

#     """    
    
#     serializer_class = EmailVerificationSerializer

#     token_param_config = openapi.Parameter(
#         'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

#     @swagger_auto_schema(manual_parameters=[token_param_config])
#     def get(self, request):
#         token = request.GET.get('token')
#         try:
#             payload = jwt.decode(
#                 token, settings.SECRET_KEY, algorithms='HS256')
#             user = User.objects.get(id=payload['user_id'])
#             if not user.is_verified:
#                 user.is_verified = True
#                 user.save()
#             return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
            
        
#         except jwt.ExpiredSignatureError as identifier:
#             return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
#         except jwt.exceptions.DecodeError as identifier:
#             return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
    
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
    

    
    
# class LoginAPIView(generics.GenericAPIView):
#     serializer_class = LoginSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#         # email = request.data['email']
#         # password = request.data['password']

#         # user = User.objects.filter(email=email).first()

#         # if user is None:
#         #     raise AuthenticationFailed('User not found!')

#         # if not user.check_password(password):
#         #     raise AuthenticationFailed('Incorrect password!')

#         # payload = {
#         #     'id': user.id,
#         #     'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#         #     'iat': datetime.datetime.utcnow()
#         # }

#         # token = jwt.encode(payload, 'secret',
#         #                    algorithm='HS256')

#         # response = Response()

#         # response.set_cookie(key='jwt', value=token, httponly=True)
#         # response.data = {
#         #     'jwt': token
#         # }
#         # return response




# class LogoutView(generics.GenericAPIView):
#     serializer_class = LogoutSerializer

#     permission_classes = (permissions.IsAuthenticated,)

#     def post(self, request):

#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(status=status.HTTP_204_NO_CONTENT)

#     # def post(self, request):
#     #     response= Response()
#     #     response.delete_cookie('jwt')
#     #     response.data = {
#     #         'message': 'logged out'
#     #     }
        
#     #     return response 
     
        
# class RequestPasswordResetEmail(generics.GenericAPIView):
#     serializer_class = ResetPasswordEmailRequestSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)

#         email = request.data.get('email', '')

#         if User.objects.filter(email=email).exists():
#             user = User.objects.get(email=email)
#             uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
#             token = PasswordResetTokenGenerator().make_token(user)
#             current_site = get_current_site(
#                 request=request).domain
#             relativeLink = reverse(
#                 'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

#             redirect_url = request.data.get('redirect_url', '')
#             absurl = 'http://'+current_site + relativeLink
#             email_body = 'Hello, \n Use link below to reset your password  \n' + \
#                 absurl+"?redirect_url="+redirect_url
#             data = {'email_body': email_body, 'to_email': user.email,
#                     'email_subject': 'Reset your passsword'}
#             Util.send_email(data)
#         return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
    

# class PasswordTokenCheckAPI(generics.GenericAPIView):
#       serializer_class = SetNewPasswordSerializer
      
#       def get(self,request,uidb64,token):
          
          
#           try:
#               id = smart_str(urlsafe_base64_decode(uidb64))
#               user=User.objects.get(id=id)
              
#               if not PasswordResetTokenGenerator().check_token(user,token):
#                   return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
              
#               return Response({'success':True,'message':'Credentials Valid', 'uidb64':uidb64,'token':token},status=status.HTTP_200_OK)
              
              
                   
#           except DjangoUnicodeDecodeError as identifier:
#               if not PasswordResetTokenGenerator():
#                 return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
    


# class SetNewPasswordAPIView(generics.GenericAPIView):
#     serializer_class=SetNewPasswordSerializer
    
#     def patch(self,request):
#         serializer =self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response({'success':True,'message':'Password reset success'},status=status.HTTP_200_OK)
    
    
    

# class GoogleSocialAuthView(GenericAPIView):

#     serializer_class = GoogleSocialAuthSerializer

#     def post(self, request):
#         """
#         POST with "auth_token"
#         Send an idtoken as from google to get user information
#         """

#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         data = ((serializer.validated_data)['auth_token'])
#         return Response(data, status=status.HTTP_200_OK)

    
# class ReservationList(ListCreateAPIView):
    
#     serializer_class = ReservationSerializer
#     queryset = Reservation.objects.all()
#     permission_classes = (permissions.IsAuthenticated,)
    
    
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
        
#     def get_queryset(self):
#         return self.queryset.filter(owner=self.request.user)



# class ReservationDetail(RetrieveUpdateDestroyAPIView):
    
#     queryset = Reservation.objects.all()
#     serializer_class = ReservationSerializer
#     permission_classes = (permissions.IsAuthenticated, IsOwner,)
#     lookup_field = 'id'
    
#     def get_queryset(self):
#         return self.queryset.filter(owner=self.request.user)
    

# class SpacesListAPIView(ListCreateAPIView):

#     serializer_class = SpacesSerializer
#     queryset = Spaces.objects.all()


