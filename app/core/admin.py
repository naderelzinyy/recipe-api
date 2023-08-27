"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# from app.core import models
from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages."""
    ordering = ["id"]
    list_display = ["email", "name"]


admin.site.register(models.User, UserAdmin)
