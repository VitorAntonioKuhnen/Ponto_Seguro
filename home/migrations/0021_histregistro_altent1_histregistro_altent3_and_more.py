# Generated by Django 4.1.7 on 2023-05-08 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_alter_histregistro_sitapr'),
    ]

    operations = [
        migrations.AddField(
            model_name='histregistro',
            name='altEnt1',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='histregistro',
            name='altEnt3',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='histregistro',
            name='altSai2',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='histregistro',
            name='altSai4',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
