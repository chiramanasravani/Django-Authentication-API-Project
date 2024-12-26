from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from djangoauthapi_app.utils import Util
from .models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


# Register Serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'tc', 'password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        # Check if the passwords match
        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords must match."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm password before creating the user
        user = get_user_model().objects.create_user(**validated_data)
        return user


# Login Serializer

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()  # Use get_user_model() for better flexibility
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        
        if not user:
            raise serializers.ValidationError('Invalid email or password.')

        if not user.is_active:
            raise serializers.ValidationError('This account is inactive.')

        attrs['user'] = user
        return attrs



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email',]



class UserChangePasswordSeializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    # confirm_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write
    class Meta:
        fields = ['password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        user = self._context.get('user')
        
        if password != confirm_password:
            raise serializers.ValidationError({"Passwords confirm_password  must match."})
        
        user.set_password(password)
        user.save()
        return attrs
    

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("Encoded UID:", uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print("Password Reset Token:", token)
            link = f'http://localhost:3000/api/user/reset/{uid}/{token}'
            print("Password Reset Link:", link)

            # Send Email
            body= 'Please use the link below to reset your password:' + link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email                                                                  
                                                                                
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError({"email": "You are not a Registered User"})





class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    # confirm_password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write
    class Meta:
        fields = ['password', 'confirm_password']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            uid = self._context.get('uid')
            token = self._context.get('token')
            
            if password != confirm_password:
                raise serializers.ValidationError({"Passwords confirm_password  must match."})
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError({"Token": "Invalid Token"})
            
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError({"Token": "Invalid Token"})

    