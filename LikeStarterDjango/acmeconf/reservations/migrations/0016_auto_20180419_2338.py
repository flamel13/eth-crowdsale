# Generated by Django 2.0.3 on 2018-04-19 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0015_auto_20180410_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventreservation',
            name='event',
            field=models.CharField(default='event', max_length=200),
        ),
    ]