# Generated by Django 5.1.1 on 2024-11-07 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_event_eventtype_event_location_alter_attendee_event_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='eventtype',
            field=models.CharField(choices=[('Public', 'Public'), ('Request To Join', 'Invite Only'), ('Private', 'Private')], default='Public', max_length=18),
        ),
    ]
