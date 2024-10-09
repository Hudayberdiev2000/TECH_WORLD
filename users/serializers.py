from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from users.models import Adddress

class UserRegistrationSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        
        validate_password(data['password'])
        return data
    
    
class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=30)
    password = serializers.CharField(write_only=True)
    
    
class AddressSerializer(serializers.Serializer):
    user = serializers.CharField(source="user.get_full_name", read_only=True)
    description = serializers.CharField(max_length=650)
    
    def create(self, validated_data):
        return Adddress.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
    

class UserSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=225)
    phone_number = serializers.CharField(max_length=30)