from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

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
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Authenticate user using the email and password
        user = authenticate(email=email, password=password)
        
        if not user:
            raise serializers.ValidationError('Invalid email or password.')

        # If authentication is successful, return the user
        attrs['user'] = user
        return attrs
