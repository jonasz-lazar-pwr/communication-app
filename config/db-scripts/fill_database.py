# Shell/Bash:
# docker exec -it backend sh
# python manage.py shell

from users.models import User, UserStatus
from conversations.models import Contact, Conversation, Message

# Tworzenie użytkowników
users = []
for i in range(1, 6):
    user = User.objects.create_user(
        username=f"user{i}",
        email=f"user{i}@example.com",
        phone_number=f"123456789{i}",
        password=f"Password123!",
        first_name=f"First{i}",
        last_name=f"Last{i}",
    )
    users.append(user)

# Tworzenie statusów użytkowników
for user in users:
    UserStatus.objects.create(
        user=user,
        status="online" if user.id % 2 == 0 else "offline",
    )

# Tworzenie kontaktów
contacts = []
for i in range(1, len(users)):
    contact = Contact.objects.create(
        user1=users[0],  # Pierwszy użytkownik jako inicjator
        user2=users[i],  # Pozostali użytkownicy jako odbiorcy
    )
    contacts.append(contact)

# Tworzenie konwersacji
conversations = []
for contact in contacts:
    conversation = Conversation.objects.create(
        contact=contact,
    )
    conversations.append(conversation)

# Tworzenie wiadomości
for conversation in conversations:
    for i in range(1, 6):  # Po 5 wiadomości na konwersację
        Message.objects.create(
            conversation=conversation,
            sender=conversation.contact.user1 if i % 2 == 0 else conversation.contact.user2,
            content=f"Sample message {i} in conversation {conversation.id}",
            is_read=i % 2 == 0,
        )

print("Database has been populated with sample data.")