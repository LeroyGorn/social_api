from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.auth_user.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True
    )

    first_name = models.CharField(
        max_length=64
    )

    last_name = models.CharField(
        max_length=64
    )

    last_activity = models.DateTimeField(
        auto_now_add=True
    )

    last_session = models.DateTimeField(
        null=True,
        blank=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
