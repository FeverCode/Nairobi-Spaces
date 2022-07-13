from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance
        )


# email = request.data['email']
        # password = request.data['password']

        # user = User.objects.filter(email=email).first()

        # if user is None:
        #     raise AuthenticationFailed('User not found!')

        # if not user.check_password(password):
        #     raise AuthenticationFailed('Incorrect password!')

        # payload = {
        #     'id': user.id,
        #     'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        #     'iat': datetime.datetime.utcnow()
        # }

        # token = jwt.encode(payload, 'secret',
        #                    algorithm='HS256')

        # response = Response()

        # response.set_cookie(key='jwt', value=token, httponly=True)
        # response.data = {
        #     'jwt': token
        # }
        # return response
