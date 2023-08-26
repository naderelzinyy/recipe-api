"""
Database models
"""
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)
from django.db import models


class UserManager(BaseUserManager):
    """Manages user table operations."""

    def create_user(self, email, password=None, **extra_fields):
        """Creates a user."""
        if not email:
            raise ValueError("User must provide email")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        # "using=db" to indicate a specific database if
        # we are using more than one.
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password):
        """Creates superuser."""
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User table structure."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
