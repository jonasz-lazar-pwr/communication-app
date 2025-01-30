# backend/conversations/models.py

from django.db import models


class Contact(models.Model):
    """Model representing a relationship between two users (contacts)."""

    user1 = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='contacts_initiated')  # Initiator
    user2 = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='contacts_received')  # Receiver
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the contact was created

    class Meta:
        managed = True
        db_table = 'contacts'
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        constraints = [
            models.UniqueConstraint(
                fields=['user1', 'user2'],
                name='unique_contacts',
                condition=models.Q(user1__lt=models.F('user2'))
            )
        ]

    def save(self, *args, **kwargs):
        """Ensure user1 has the smaller ID to enforce consistent ordering."""
        if self.user1.id > self.user2.id:  # Swap users if necessary
            self.user1, self.user2 = self.user2, self.user1
        super().save(*args, **kwargs)

    def __str__(self):
        """Return a string representation of the contact."""
        return f"contact between {self.user1.username} and {self.user2.username}"


class Conversation(models.Model):
    """Model representing a conversation between two users."""

    contact = models.OneToOneField(Contact, on_delete=models.CASCADE, related_name='conversation')  # Associated contact
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the conversation was created

    class Meta:
        managed = True
        db_table = 'conversations'
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"

    def __str__(self):
        """Return a string representation of the conversation."""
        return f"conversation for {self.contact}"


class Message(models.Model):
    """Model representing a message within a conversation."""

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')  # Associated conversation
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='sent_messages')  # Sender of the message
    content = models.TextField()  # Content of the message
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the message was sent
    is_read = models.BooleanField(default=False)  # Whether the message has been read

    class Meta:
        managed = True
        db_table = 'messages'
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        indexes = [
            models.Index(fields=['conversation', 'created_at']),  # Index for efficient chronological queries
        ]

    def __str__(self):
        """Return a string representation of the message."""
        return f"message from {self.sender.username} in conversation: {self.conversation}"
