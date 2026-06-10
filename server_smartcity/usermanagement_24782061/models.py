from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Field kustom sesuai instruksi Lab 6
    is_admin = models.BooleanField(default=False)
    is_member = models.BooleanField(default=True)

    def __str__(self):
        return self.username