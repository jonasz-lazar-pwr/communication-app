# backend/conversations/admin.py

from django.contrib import admin
from .models import Contact, Conversation, Message


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin configuration for the Contact model."""
    list_display = [
        'id',
        'user1',
        'user2',
        'created_at'
    ]

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Admin configuration for the Conversation model."""
    list_display = [
        'id',
        'contact',
        'created_at'
    ]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin configuration for the Message model."""
    list_display = [
        'id',
        'conversation',
        'sender',
        'is_read',
        'content',
        'created_at'
    ]