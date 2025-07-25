# users/sms.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SMS_API_KEY")  # ключ из .env

def send_sms_code(phone, code):
    message = f"Ваш код: {code}"
    response = requests.get(
        "https://sms.ru/sms/send",
        params={
            "api_id": API_KEY,
            "to": phone,
            "msg": message,
            "json": 1
        }
    )
    result = response.json()
    if result['status'] != 'OK':
        print("[ERROR] Ошибка при отправке СМС:", result)
    else:
        print(f"[OK] СМС отправлена на {phone}")
