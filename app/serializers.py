import email
from app.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        
        
    def validate(self,attrs):
            email = attrs.get('email', '')
            username = attrs.get('username', '')
            

            if not username.isalnum():
                raise serializers.ValidationError(
                   'The username must be alphanumeric.')
            return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)   
                
          

    


class LoginSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token')

        read_only_fields = ['token']
        
        
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']
