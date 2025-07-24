# Test Task - Referral System

### Эндпоинты:

- `POST /api/auth/request-code/`
  - Вход: `{"phone_number": "79991112233"}`
  - Выход: `{"message": "Код отправлен"}`

- `POST /api/auth/verify-code/`
  - Вход: `{"phone_number": "79991112233", "code": "1234"}`
  - Выход: Пользователь с инвайт-кодом

- `POST /api/activate-code/`
  - Вход: `{"phone_number": "79991112233", "invite_code": "ABC123"}`
  - Выход: `{"message": "Инвайт-код активирован"}`

- `GET /api/users/`
  - Список пользователей и их инвайт-кодов

---

### Как запустить

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
