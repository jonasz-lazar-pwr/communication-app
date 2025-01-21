# backend/users/admin.py

from django.contrib import admin
from .models import User, UserStatus


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin configuration for the User model."""
    list_display = [field.name for field in User._meta.fields]


@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    """Admin configuration for the UserStatus model."""
    list_display = [field.name for field in UserStatus._meta.fields]
