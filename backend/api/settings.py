"""
Django settings for api project.
"""

from pathlib import Path
from decouple import config

# === Paths and Directories ===
# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# === Security Settings ===
# Secret key for Django
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET_KEY', default='fallback_key')

# Debug mode
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DJANGO_DEBUG', cast=bool, default=True)

# Allowed hosts
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default='').split(',')

# === HTTPS and SSL Settings ===
# Enforce HTTPS (use True in production)
SECURE_SSL_REDIRECT = True
# Header for detecting HTTPS when using a proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Paths to SSL certificates
SSL_CERT_PATH = BASE_DIR / 'certs' / 'localhost-cert.pem'
SSL_KEY_PATH = BASE_DIR / 'certs' / 'localhost-key.pem'

# Path to RSA private key (used for OpenID Connect)
OIDC_RSA_PRIVATE_KEY_PATH = BASE_DIR / 'certs' / 'private-key.pem'

# Load RSA private key content
with open(OIDC_RSA_PRIVATE_KEY_PATH, 'r') as f:
    OIDC_RSA_PRIVATE_KEY = f.read()

# === Installed Applications ===
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions', # For development tools (runserver_plus)
    'corsheaders', # For handling CORS
    'rest_framework', # Django REST framework
    'oauth2_provider', # OAuth Toolkit
    'users', # Custom users app
    'conversations', # Conversations app
]

# === Middleware ===
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Handles CORS headers
    'django.middleware.security.SecurityMiddleware',  # Handles security headers
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session management
    'django.middleware.common.CommonMiddleware',  # Common HTTP functionalities
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Authentication
    'django.contrib.messages.middleware.MessageMiddleware',  # Message framework
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
    'oauth2_provider.middleware.OAuth2TokenMiddleware',  # OAuth2 middleware
]

# === URL and WSGI Configuration ===
ROOT_URLCONF = 'api.urls'
WSGI_APPLICATION = 'api.wsgi.application'

# === Templates Configuration ===
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# === REST Framework Configuration ===
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication', # OAuth authentication
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated', # Require authentication by default
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
}

# === Database Configuration ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', cast=int),
    }
}

# === Password Validation ===
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# === Internationalization and Localization ===
LANGUAGE_CODE = 'en-us'  # Language setting
TIME_ZONE = 'Europe/Warsaw'  # Time zone
USE_I18N = True  # Enable internationalization
USE_TZ = True  # Enable timezone support

# === Static Files ===
STATIC_URL = 'static/'  # URL for static files

# === Default Primary Key Field ===
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# === CORS Configuration ===
CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins (use cautiously in production)

# === OAuth2 Provider Configuration ===
OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 900,  # Access token expiration (15 minutes)
    'REFRESH_TOKEN_EXPIRE_SECONDS': 86400,  # Refresh token expiration (1 day)
    'ROTATE_REFRESH_TOKENS': True,  # Rotate refresh tokens after use
    'OIDC_ENABLED': True,  # Enable OpenID Connect
    'OIDC_RSA_PRIVATE_KEY': OIDC_RSA_PRIVATE_KEY,  # RSA private key for OpenID Connect
    'SCOPES': {
        'openid': 'OpenID Connect scope',
        'read': 'Read access',
        'write': 'Write access',
        'offline_access': 'Offline access',
    },
    'PKCE_REQUIRED': True,  # PKCE required for authorization code flow
    'ALLOWED_REDIRECT_URI_SCHEMES': ['https'],  # Allowed redirect URI schemes
}

# === Cookies Security Settings ===
SESSION_COOKIE_HTTPONLY = True # Cookie nie jest dostępne dla JavaScript. Chroni przed atakami XSS
SESSION_COOKIE_SECURE = True  # Cookie jest wysyłane tylko przez HTTPS, nie przez HTTP. Bardzo ważne w produkcji

# === CORS Configuration ===
CORS_ALLOW_CREDENTIALS = True  # Pozwala na wysyłanie cookies między domenami (cookies w requestach fetch() / axios().)
CORS_ALLOWED_ORIGINS = [
    "https://localhost:4200",  # Dozwolony frontend (Angular)
"   https://127.0.0.1:4200",
]

# === Authentication Configuration ===
AUTH_USER_MODEL = 'users.User'  # Custom user model
AUTHENTICATION_BACKENDS = [
    'users.backends.CustomAuthBackend',  # Custom authentication backend
    'oauth2_provider.backends.OAuth2Backend',  # OAuth2 authentication backend
]

# === Logging Configuration for Werkzeug ===
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {  # Log to console
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'werkzeug': {  # Werkzeug debugger logs
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# === Runserver Plus Configuration ===
RUNSERVERPLUS_SERVER_ADDRESS_PORT = '0.0.0.0:8000'  # Server binding configuration
