from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    default_password = models.BooleanField(default=True)  # Track if password needs changing
    def __str__(self):
        return self.username