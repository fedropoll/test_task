# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import EmailSerializer, VerifySerializer, UserSerializer, ActivateCodeSerializer
from .email_sender import send_email_code  # Импортируем новую функцию
import random

TEMP_CODES = {}

class RequestCodeView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = str(random.randint(1000, 9999))
            TEMP_CODES[email] = code
            send_email_code(email, code) # Отправляем код на email
            print(f"[DEBUG] Код для {email}: {code}")
            return Response({'message': 'Код отправлен'}, status=201)
        return Response(serializer.errors, status=400)

class VerifyCodeView(APIView):
    def post(self, request):
        serializer = VerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            if TEMP_CODES.get(email) == code:
                # Используем get_or_create с email, так как теперь это USERNAME_FIELD
                user, created = User.objects.get_or_create(email=email, username=email)
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
            email = serializer.validated_data['email']
            code = serializer.validated_data['invite_code']

            try:
                user = User.objects.get(email=email)
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