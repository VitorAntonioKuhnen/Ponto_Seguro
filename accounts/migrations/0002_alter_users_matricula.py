# Generated by Django 4.1.7 on 2023-04-01 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='matricula',
            field=models.IntegerField(unique=True),
        ),
    ]
