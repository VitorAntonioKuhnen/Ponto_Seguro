# Generated by Django 4.1.7 on 2023-04-08 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_escala_horaentm_alter_escala_horaentv_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='histregistro',
            old_name='sitReg',
            new_name='sitAPR',
        ),
    ]
