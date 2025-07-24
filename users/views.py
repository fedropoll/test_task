from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import PhoneSerializer, VerifySerializer, UserSerializer
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
            return Response({'message': 'Код отправлен'})
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
                return Response(UserSerializer(user).data)
            return Response({'error': 'Неверный код'}, status=400)
        return Response(serializer.errors, status=400)

class ActivateCodeView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        code = request.data.get('invite_code')

        if not phone or not code:
            return Response({'error': 'Телефон и код обязательны'}, status=400)

        try:
            user = User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=404)

        if user.activated_code:
            return Response({'error': 'Инвайт уже активирован'}, status=400)

        if not User.objects.filter(invite_code=code).exists():
            return Response({'error': 'Код не найден'}, status=404)

        if code == user.invite_code:
            return Response({'error': 'Нельзя активировать свой код'}, status=400)

        user.activated_code = code
        user.save()
        return Response({'message': 'Инвайт-код активирован'}, status=200)

class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        data = [{'phone_number': u.phone_number, 'invite_code': u.invite_code} for u in users]
        return Response(data)
