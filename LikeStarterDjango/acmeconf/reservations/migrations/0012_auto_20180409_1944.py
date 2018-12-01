# Generated by Django 2.0.3 on 2018-04-09 17:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0011_auto_20180409_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventreservation',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='Unique ID for the reservation', primary_key=True, serialize=False),
        ),
    ]