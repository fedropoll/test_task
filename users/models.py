from django.contrib.auth.models import AbstractUser
from django.db import models
import random, string

def generate_invite_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class User(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    invite_code = models.CharField(max_length=6, unique=True, default=generate_invite_code)
    activated_code = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number
