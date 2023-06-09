# Generated by Django 4.1.7 on 2023-04-11 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_users_hora_extra_alter_users_justificar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nmCargo', models.CharField(max_length=100)),
                ('sitCargo', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Cargo',
                'verbose_name_plural': 'Cargos',
                'db_table': 'cargo',
            },
        ),
    ]
