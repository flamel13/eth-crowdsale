# Generated by Django 2.0.3 on 2018-04-05 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_eventreservation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventreservation',
            name='reservation',
        ),
    ]