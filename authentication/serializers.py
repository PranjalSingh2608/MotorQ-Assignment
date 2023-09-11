from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
import re
from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    phoneNumber=serializers.CharField(validators=[
        validators.RegexValidator(
            regex='^\d{10}$',
            message='Mobile number must be 10 digits long.',
            code='invalid_mobile_number'
        ),
    ])
    password=serializers.CharField()

    def validate(self,data):
        if data['phoneNumber']:
            if User.objects.filter(username=data['phoneNumber']).exists():
                raise serializers.ValidationError("phone number already exists")
            
        return data
    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(char.isalpha() for char in value) or \
           not any(char.isdigit() for char in value) or \
           not any(char in "!@#$%^&*()_-+=<>?/[]{}" for char in value):
            raise ValidationError("Password must contain at least one alphabet, one number, and one special character.")

        return value

    def create(self, validated_data):
        user=User.objects.create_user(username=validated_data['phoneNumber'], password=validated_data['password'])
        user.save()

        return validated_data
    

class LoginSerializer(serializers.Serializer):
    phoneNumber=serializers.CharField()
    password=serializers.CharField()