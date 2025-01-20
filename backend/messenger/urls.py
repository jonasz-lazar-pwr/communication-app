from django.urls import path
from .views import test_message

urlpatterns = [
    path('hello/', test_message, name='hello'),
]