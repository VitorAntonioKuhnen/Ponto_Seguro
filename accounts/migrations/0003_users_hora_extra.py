# Generated by Django 4.1.7 on 2023-04-09 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='hora_extra',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]