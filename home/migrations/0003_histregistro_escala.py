# Generated by Django 4.1.7 on 2023-04-08 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_escala_nmescala'),
    ]

    operations = [
        migrations.AddField(
            model_name='histregistro',
            name='escala',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='home.escala'),
        ),
    ]
