# Generated by Django 5.1.1 on 2024-11-21 09:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_event_eventtype'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventinvite',
            old_name='invitee',
            new_name='invitor',
        ),
    ]
