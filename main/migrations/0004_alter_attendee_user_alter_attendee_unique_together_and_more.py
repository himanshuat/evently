# Generated by Django 5.1.1 on 2024-11-05 08:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_rating_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='attendee',
            unique_together={('user', 'event')},
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together={('user', 'event')},
        ),
    ]
