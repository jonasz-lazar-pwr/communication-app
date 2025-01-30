# backend/users/admin.py

from django.contrib import admin
from .models import User, UserStatus


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin configuration for the User model."""
    list_display = [
        'id',
        'username',
        'email',
        'phone_number',
        'first_name',
        'last_name',
        'is_active',
        'sub',
        'last_login',
        'profile_picture',
        'is_superuser',
        'is_staff',
        'created_at',
        'modified_at'
    ]


@admin.register(UserStatus)
class UserStatusAdmin(admin.ModelAdmin):
    """Admin configuration for the UserStatus model."""
    list_display = [
        'user',
        'status',
    ]

# list_display = [field.name for field in User._meta.fields]
