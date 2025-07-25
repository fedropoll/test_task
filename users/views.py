from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import PhoneSerializer, VerifySerializer, UserSerializer, ActivateCodeSerializer
import random

TEMP_CODES = {}

class RequestCodeView(APIView):
    def post(self, request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']
            code = str(random.randint(1000, 9999))
            TEMP_CODES[phone] = code
            print(f"[DEBUG] Код для {phone}: {code}")
            return Response({'message': 'Код отправлен'}, status=201)
        return Response(serializer.errors, status=400)

class VerifyCodeView(APIView):
    def post(self, request):
        serializer = VerifySerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']
            if TEMP_CODES.get(phone) == code:
                user, created = User.objects.get_or_create(phone_number=phone, username=phone)
                user.is_verified = True
                if created:
                    user.set_unusable_password()
                user.save()
                return Response(UserSerializer(user).data, status=201)
            return Response({'error': 'Неверный код'}, status=400)
        return Response(serializer.errors, status=400)

class ActivateCodeView(APIView):
    def post(self, request):
        serializer = ActivateCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone_number']
            code = serializer.validated_data['invite_code']

            try:
                user = User.objects.get(phone_number=phone)
            except User.DoesNotExist:
                return Response({'error': 'Пользователь не найден'}, status=404)

            if user.activated_code:
                return Response({'error': 'Инвайт уже активирован'}, status=400)

            if code == user.invite_code:
                return Response({'error': 'Нельзя активировать свой код'}, status=400)

            if not User.objects.filter(invite_code=code).exists():
                return Response({'error': 'Код не найден'}, status=404)

            user.activated_code = code
            user.save()
            return Response({'message': 'Инвайт-код активирован'}, status=200)

        return Response(serializer.errors, status=400)

class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=200)
