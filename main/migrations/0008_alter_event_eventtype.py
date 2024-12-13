# Generated by Django 5.1.1 on 2024-11-11 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_event_eventtype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='eventtype',
            field=models.CharField(choices=[('Public', 'Public'), ('Request To Join', 'Request To Join'), ('Invite Only', 'Invite Only')], default='Public', max_length=18),
        ),
    ]
