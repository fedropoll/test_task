from rest_framework import serializers
from .models import User

class PhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)

class VerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=4)

class ActivateCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    invite_code = serializers.CharField(max_length=6)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'invite_code', 'activated_code', 'is_verified']
