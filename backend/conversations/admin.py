# backend/conversations/admin.py

from django.contrib import admin
from .models import Contact, Conversation, Message


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin configuration for the Contact model."""
    list_display = [field.name for field in Contact._meta.fields]


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Admin configuration for the Conversation model."""
    list_display = [field.name for field in Conversation._meta.fields]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin configuration for the Message model."""
    list_display = [field.name for field in Message._meta.fields]
