# users/email_sender.py
from django.core.mail import send_mail
from django.conf import settings

def send_email_code(email, code):
    subject = "Ваш код авторизации"
    message = f"Здравствуйте! Ваш код для входа: {code}"
    email_from = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    try:
        send_mail(subject, message, email_from, recipient_list)
        print(f"[OK] Email с кодом отправлен на {email}")
    except Exception as e:
        print(f"[ERROR] Ошибка при отправке email: {e}")