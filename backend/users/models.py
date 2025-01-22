# backend/users/models.py

from django.db import models


class User(models.Model):
    """Model representing a user in the application."""

    username = models.CharField(max_length=50, unique=True)  # Unique username for the user
    email = models.EmailField(unique=True)  # Unique email address
    phone_number = models.CharField(max_length=15, unique=True)  # Unique phone number
    password_hash = models.CharField(max_length=255)  # Hashed password for authentication
    first_name = models.CharField(max_length=50)  # User's first name
    last_name = models.CharField(max_length=50)  # User's last name
    profile_picture = models.TextField(null=True, blank=True)  # Optional profile picture URL
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the user was created
    modified_at = models.DateTimeField(auto_now=True)  # Timestamp of the last modification

    class Meta:
        managed = True
        db_table = 'users'
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        """Return a string representation of the user."""
        return self.username


class UserStatus(models.Model):
    """Model representing a user's online/offline status."""

    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)  # Reference to the user
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='offline')  # Online/offline status
    last_active = models.DateTimeField(auto_now=True)  # Timestamp of the user's last activity

    class Meta:
        managed = True
        db_table = 'users_status'
        verbose_name = "User status"
        verbose_name_plural = "Users status"

    def __str__(self):
        """Return a string representation of the user's status."""
        return f"{self.user.username} - {self.status}"
