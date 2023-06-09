# Generated by Django 4.1.7 on 2023-04-08 13:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Escala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horaEntM', models.TimeField()),
                ('horaSaiM', models.TimeField()),
                ('horaEntV', models.TimeField()),
                ('horaSaiV', models.TimeField()),
                ('status', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Escala',
                'verbose_name_plural': 'Escalas',
                'db_table': 'escala',
            },
        ),
        migrations.CreateModel(
            name='TipoJustificativa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoJustificativa', models.CharField(max_length=70)),
                ('sitJust', models.BooleanField()),
            ],
            options={
                'verbose_name': 'Tipo de Justificativa',
                'verbose_name_plural': 'Tipos de Justificativas',
                'db_table': 'tipojustificativa',
            },
        ),
        migrations.CreateModel(
            name='Justificativa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('hora', models.TimeField()),
                ('tipoJust', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='home.tipojustificativa')),
                ('userReg', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Justificativa',
                'verbose_name_plural': 'Justificativas',
                'db_table': 'justificativa',
            },
        ),
        migrations.CreateModel(
            name='HistRegistro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataReg', models.DateField()),
                ('horaEntM', models.TimeField()),
                ('horaSaiM', models.TimeField()),
                ('horaEntV', models.TimeField()),
                ('horaSaiV', models.TimeField()),
                ('bancoHora', models.TimeField()),
                ('sitReg', models.BooleanField()),
                ('userReg', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Histórico de Registro',
                'verbose_name_plural': 'Histórico de Registros',
                'db_table': 'histregistro',
            },
        ),
    ]
