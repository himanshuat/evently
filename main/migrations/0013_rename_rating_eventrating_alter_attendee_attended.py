# Generated by Django 5.1.1 on 2024-11-23 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_event_eventtype'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Rating',
            new_name='EventRating',
        ),
        migrations.AlterField(
            model_name='attendee',
            name='attended',
            field=models.CharField(choices=[('Yes', 'Yes'), ('No', 'No'), ('Unknown', 'Unknown')], default='Unknown', max_length=10),
        ),
    ]
