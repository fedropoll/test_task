# users/serializers.py
from rest_framework import serializers
from .models import User

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=4)

class ActivateCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    invite_code = serializers.CharField(max_length=6)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'invite_code', 'activated_code', 'is_verified']