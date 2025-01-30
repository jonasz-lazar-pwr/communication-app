# backend/api/urls.py

"""
URL configuration for api project.
"""
from django.contrib import admin
from django.urls import path, include
from oauth2_provider.views import AuthorizationView

from users.views import CustomLoginView, CustomTokenView, CustomLogoutAndRevokeTokenView, CustomUserInfoView

oauth_urlpatterns = [
    path('api/user/oauth/login/', CustomLoginView.as_view(), name='login'),
    path('api/user/oauth/authorize/', AuthorizationView.as_view(), name='authorize'),
    path('api/user/oauth/token/', CustomTokenView.as_view(), name='token'),
    path('api/user/oauth/logout/', CustomLogoutAndRevokeTokenView.as_view(), name='logout_revoke_token'),
    path('api/user/oauth/userinfo/', CustomUserInfoView.as_view(), name='info'),
    path('api/user/oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('users.urls')),
]

urlpatterns += oauth_urlpatterns