# backend/users/views.py

import json

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from oauth2_provider.oauth2_backends import get_oauthlib_core
from oauth2_provider.models import RefreshToken

from users.permissions import IsAuthenticatedViaCookie


class CustomLoginView(APIView):
    """
    Handles user authentication and login using email or phone number.
    If authentication is successful, a session is created.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Extracts user credentials from request
        login_input = request.data.get('login_input')
        password = request.data.get('password')

        # Authenticates user using the custom authentication backend
        user = authenticate(request, login_input=login_input, password=password)
        if user:
            login(request, user)  # Creates a Django session
            return Response({"detail": "Authenticated"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class CustomLogoutAndRevokeTokenView(APIView):
    """
    Logs out the user and revokes OAuth2 tokens:
    - Ends Django session
    - Removes access_token and refresh_token from cookies
    - Revokes OAuth2 tokens stored in the database
    """
    permission_classes = [IsAuthenticatedViaCookie]

    def post(self, request, *args, **kwargs):
        # Logs out the user and terminates the session
        if request.user.is_authenticated:
            logout(request)

        # Retrieves refresh token from cookies
        refresh_token_cookie = request.COOKIES.get("refresh_token")

        # Revokes the refresh token if it exists
        if refresh_token_cookie:
            try:
                refresh_token = RefreshToken.objects.get(token=refresh_token_cookie)
                refresh_token.revoke()  # Revokes both refresh and associated access tokens
            except RefreshToken.DoesNotExist:
                pass  # Ignore if token does not exist in the database

        # Builds response
        response = Response({"detail": "Successfully logged out and tokens revoked"}, status=status.HTTP_200_OK)

        # Removes access and refresh tokens from cookies
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        response.delete_cookie("sessionid")

        return response



class CustomTokenView(APIView):
    """
    Handles OAuth2 token requests.
    Supports:
    - Authorization code flow (PKCE)
    - Refresh token flow
    Stores tokens in HttpOnly cookies and removes them from response body.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Extracts grant type from request
        grant_type = request.data.get("grant_type")

        # If refresh_token is used, retrieve it from cookies if not provided in request body
        if grant_type == "refresh_token":
            if "refresh_token" not in request.data:
                cookie_refresh = request.COOKIES.get("refresh_token")
                if not cookie_refresh:
                    return Response({"detail": "No refresh token found"}, status=status.HTTP_400_BAD_REQUEST)

                # Modify request data so that OAuth2 library can process it
                mutable_data = request.data.copy()
                mutable_data["refresh_token"] = cookie_refresh
                request._request.POST = mutable_data

        elif grant_type == "authorization_code":
            # No modifications needed, OAuth2 will handle validation
            pass

        else:
            # Unsupported grant type
            return Response({"detail": "Unsupported grant_type"}, status=status.HTTP_400_BAD_REQUEST)

        # Generates token response using OAuth2
        oauthlib_core = get_oauthlib_core()
        uri, headers, body, status_code = oauthlib_core.create_token_response(request._request)

        # Builds the response
        response = HttpResponse(content=body, status=status_code)
        for k, v in headers.items():
            response[k] = v

        # If successful, extract tokens and store them in cookies
        if status_code == 200:
            token_data = json.loads(body)

            access_token = token_data.pop("access_token", None)
            refresh_token = token_data.pop("refresh_token", None)
            token_data.pop("id_token", None)  # Optionally remove id_token

            # Remaining response contains only metadata like expires_in, scope, token_type
            response.content = json.dumps(token_data)

            if access_token:
                response.set_cookie(
                    key="access_token",
                    value=access_token,
                    httponly=True,
                    secure=True,
                    samesite="None",  # Required for CORS scenarios
                )
            if refresh_token:
                print(f"Received refresh_token: {refresh_token}")
                response.set_cookie(
                    key="refresh_token",
                    value=refresh_token,
                    httponly=True,
                    secure=True,
                    samesite="None",
                )

        return response


class CustomUserInfoView(APIView):
    """
    Custom /userinfo/ endpoint that returns user details based on the access token.
    """
    permission_classes = [IsAuthenticatedViaCookie]

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user or not user.is_authenticated:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        return JsonResponse({
            "sub": str(user.sub),  # Unique identifier for the user (OIDC standard)
            "username": user.username,
            "email": user.email,
            "phone_number": user.phone_number,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profile_picture": user.profile_picture,
        })
