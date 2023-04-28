# Generated by Django 4.1.7 on 2023-04-09 15:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0007_rename_horaentm_escala_horent1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='horaextra',
            name='userLib',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='userLib', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='horaextra',
            name='userExtra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='userExtra', to=settings.AUTH_USER_MODEL),
        ),
    ]