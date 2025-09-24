from django.contrib.auth.models  import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('carpenter', 'Carpenter'),
        ('customer', 'Customer'),
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='Customer')
    email = models.EmailField()


