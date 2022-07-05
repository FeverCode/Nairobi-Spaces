from app.models import User
from rest_framework import serializers



# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'password']
#         extra_kwargs = {'password': {'write_only': True, 'required': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
