# Generated by Django 4.1.7 on 2023-05-10 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0023_remove_justificativa_histregistro_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='histregistro',
            name='justificativas',
        ),
        migrations.AddField(
            model_name='histregistro',
            name='justificativas',
            field=models.ManyToManyField(blank=True, null=True, to='home.justificativa'),
        ),
    ]
