# Generated by Django 2.0.3 on 2018-11-09 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0040_auto_20181108_0800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='like_user_set', to=settings.AUTH_USER_MODEL),
        ),
    ]