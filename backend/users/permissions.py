# backend/users/permissions.py

from django.utils.timezone import now
from rest_framework.permissions import BasePermission
from oauth2_provider.models import AccessToken

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class IsAuthenticatedViaCookie(BasePermission):
    """
    Grants access only to users with a valid access token stored in cookies.
    """

    def has_permission(self, request, view):
        """
        Checks if the user has a valid access token in cookies.

        Args:
            request (HttpRequest): The incoming request.
            view (APIView): The view being accessed.

        Returns:
            bool: True if the user has a valid token, otherwise False.
        """
        access_token = request.COOKIES.get("access_token")
        if not access_token:
            return False  # Deny access if no access token is found in cookies

        try:
            # Retrieve the token and ensure it is still valid (not expired)
            token = AccessToken.objects.get(token=access_token, expires__gt=now())
            # Assign the authenticated user to the request
            request.user = token.user
            request.resource_owner = token.user  # Compatibility with OAuth2 views
            return True
        except AccessToken.DoesNotExist:
            return False  # Deny access if the token does not exist or is expired


class IsAdminUserViaCookie(IsAuthenticatedViaCookie):
    """
    Grants access only to admin users with a valid access token in cookies.
    """

    def has_permission(self, request, view):
        """
        Checks if the user is authenticated and has admin privileges.

        Args:
            request (HttpRequest): The incoming request.
            view (APIView): The view being accessed.

        Returns:
            bool: True if the user is an admin, otherwise False.
        """
        # First, ensure the user is authenticated via the cookie-based access token
        if super().has_permission(request, view):
            return request.user.is_staff  # Allow access only if the user is an admin
        return False


class IsAuthenticatedOrReadOnlyViaCookie(IsAuthenticatedViaCookie):
    """
    Allows unauthenticated users to perform read-only operations (GET, HEAD, OPTIONS).
    Authenticated users can perform any request.
    """

    def has_permission(self, request, view):
        """
        Checks if the request is either read-only or the user is authenticated.

        Args:
            request (HttpRequest): The incoming request.
            view (APIView): The view being accessed.

        Returns:
            bool: True if the request is read-only or the user is authenticated.
        """
        return request.method in SAFE_METHODS or super().has_permission(request, view)


class IsOwnerOrAdmin(BasePermission):
    """
    Grants access to a resource only if the requesting user is the owner or an admin.
    """

    def has_object_permission(self, request, view, obj):
        """
        Checks if the requesting user is the owner of the object or an admin.

        Args:
            request (HttpRequest): The incoming request.
            view (APIView): The view being accessed.
            obj (Model instance): The object being accessed.

        Returns:
            bool: True if the user is the owner or an admin, otherwise False.
        """
        return request.user == obj or request.user.is_staff