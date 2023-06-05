# from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
# from models import RegistroPonto


# class Command(BaseCommand):
#     help = 'Cria registros zerados para pessoas sem registro de ponto'

#     def handle(self, *args, **options):
#         print('Printou pois foi acionado pelo CronTab')
        # Lógica para criar registros zerados
        # pessoas_sem_registro = User.objects.filter(registroponto__isnull=True)
        
        # for pessoa in pessoas_sem_registro:
            # RegistroPonto.objects.create(usuario=pessoa, registro=0)

import os
import django
import fcntl

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PONTO_SEGURO.settings')
django.setup()

from django.contrib.auth.models import User
# from seuapp.models import RegistroPonto


def criar_registros_zerados():
    # Lógica para criar registros zerados
    # pessoas_sem_registro = User.objects.filter(registroponto__isnull=True)

    # for pessoa in pessoas_sem_registro:
    #     RegistroPonto.objects.create(usuario=pessoa, registro=0)
    print('Printou pois foi acionado pelo CronTab')


criar_registros_zerados()