# Generated by Django 4.1.7 on 2023-05-27 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_horaextra_justificativas'),
    ]

    operations = [
        migrations.AddField(
            model_name='histregistro',
            name='tipo',
            field=models.CharField(default=1, max_length=2),
            preserve_default=False,
        ),
    ]
