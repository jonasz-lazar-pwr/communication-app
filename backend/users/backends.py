# backend/users/backends.py

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from users.models import User


class CustomAuthBackend(ModelBackend):
    """
    Custom authentication backend that allows authentication using either email or phone number.
    The standard Django username authentication is disabled.
    """

    def authenticate(self, request, login_input=None, password=None, **kwargs):
        """
        Authenticates a user using their email or phone number instead of a traditional username.

        Args:
            request (HttpRequest): The request object.
            login_input (str, optional): The email or phone number used for authentication.
            password (str, optional): The user's password.

        Returns:
            User instance if authentication is successful, otherwise None.
        """
        try:
            # Ensure the username field is either an email or phone number, not a traditional username.
            user = User.objects.get(Q(email=login_input) | Q(phone_number=login_input))
        except User.DoesNotExist:
            return None  # If no user is found, return None

        # Verify the provided password
        if user.check_password(password):
            return user  # Return the authenticated user instance
        return None  # Return None if the password is incorrect