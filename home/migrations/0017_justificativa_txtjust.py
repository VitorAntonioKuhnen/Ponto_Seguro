# Generated by Django 4.1.7 on 2023-04-22 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_alter_histregistro_bancohoramin'),
    ]

    operations = [
        migrations.AddField(
            model_name='justificativa',
            name='txtJust',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]