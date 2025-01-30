# backend/users/models.py
import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.db import models


class UserManager(BaseUserManager):
    """Custom manager for User model."""
    def create_user(self, username, email, phone_number, password=None, **extra_fields):
        """Create and return a regular user."""
        if not username:
            raise ValueError('The Username field must be set.')
        if not email:
            raise ValueError('The Email field must be set.')
        if not phone_number:
            raise ValueError('The Phone Number field must be set.')
        if not password:
            raise ValueError('The Password field must be set.')

        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        # Create user
        user = self.model(
            username=username,
            email=email,
            phone_number=phone_number,
            **extra_fields
        )
        user.set_password(password)  # Hash password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, phone_number, password=None, **extra_fields):
        """Create and return a superuser."""
        if not username:
            raise ValueError('The Username field must be set.')
        if not email:
            raise ValueError('The Email field must be set.')
        if not phone_number:
            raise ValueError('The Phone Number field must be set.')
        if not password:
            raise ValueError('The Password field must be set.')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Create superuser
        return self.create_user(
            username=username,
            email=email,
            phone_number=phone_number,
            password=password,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model."""
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    sub = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    profile_picture = models.TextField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True,
        help_text="The groups this user belongs to.",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'username', 'first_name', 'last_name']

    class Meta:
        managed = True
        db_table = 'users'
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        """Return a string representation of the user."""
        return f"{self.username}"


class UserStatus(models.Model):
    """Model representing a user's online/offline status."""
    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='status')  # Reference to the user
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='offline')  # Online/offline status

    class Meta:
        managed = True
        db_table = 'users_status'
        verbose_name = "User status"
        verbose_name_plural = "Users status"

    def __str__(self):
        """Return a string representation of the user status."""
        return f"status of {self.user.username}: {self.status}"

