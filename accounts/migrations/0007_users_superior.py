# Generated by Django 4.1.7 on 2023-05-01 15:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_users_cargo'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='superior',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
