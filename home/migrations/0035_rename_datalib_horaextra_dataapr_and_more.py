# Generated by Django 4.1.7 on 2023-06-11 20:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0034_histregistro_obssup_horaextra_obssup'),
    ]

    operations = [
        migrations.RenameField(
            model_name='horaextra',
            old_name='dataLib',
            new_name='dataApr',
        ),
        migrations.RemoveField(
            model_name='horaextra',
            name='userLib',
        ),
        migrations.AddField(
            model_name='histregistro',
            name='dataApr',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='histregistro',
            name='userApr',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='userApr', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='horaextra',
            name='userAprHe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='userAprHe', to=settings.AUTH_USER_MODEL),
        ),
    ]
