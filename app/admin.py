from django.contrib import admin

from app.models import SubscribedUsers, Profile, Reservation, Reviews, Spaces, User

# Register your models here.
admin.site.register(Spaces)
admin.site.register(Reservation)
admin.site.register(Profile)
admin.site.register(SubscribedUsers)
admin.site.register(Reviews)

