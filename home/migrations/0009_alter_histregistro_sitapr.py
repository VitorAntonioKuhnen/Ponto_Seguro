# Generated by Django 4.1.7 on 2023-04-09 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_horaextra_userlib_alter_horaextra_userextra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='histregistro',
            name='sitAPR',
            field=models.BooleanField(default=False),
        ),
    ]
