# Generated by Django 5.1.5 on 2025-01-21 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options_alter_userstatus_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userstatus',
            options={'verbose_name': 'User status', 'verbose_name_plural': 'Users statuses'},
        ),
    ]
