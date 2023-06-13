from home.models import Feriado, HistRegistro, Escala
from accounts.models import Users
from datetime import datetime as hora, datetime as data, timedelta
from django.db.models import Q
from decouple import config
import requests


def get_api_feriados():
  resposta = requests.get(f'https://api.invertexto.com/v1/holidays/2023?token={config("TOKEN")}&state=SC')
  if resposta.status_code == 200:
      json = resposta.json()
      if json:
          for feriado in json:
              
              if feriado['type'] == 'facultativo':
                tipo = 1

              elif feriado['type'] == 'feriado':
                tipo = 2

              if feriado['level'] == 'nacional':   
                level = 1

              Feriado.objects.create(data= feriado['date'], nome=feriado['name'], tipo_id = tipo, level_id = level)
  
  else:
      print('Ocorreu um erro ao carregar os dados da nova')        


def gera_escala_zerada():
   feriado = Feriado.objects.filter(data = (data.today().date() - timedelta(days=1)))
   if not feriado:
      for user in Users.objects.filter(dat_inicia_trab__lte=(data.today().date() - timedelta(days=1)), is_active = True):
        if not HistRegistro.objects.filter(userReg_id = user.id, dataReg = (data.today().date() - timedelta(days=1))).exists():
          print('Precisa criar registro')
          numDiaSemana = data.today().weekday()
          if numDiaSemana == 0:
              diaSemana = user.escala.segunda
          elif numDiaSemana == 1:
              diaSemana = user.escala.terca
          elif numDiaSemana == 2:
              diaSemana = user.escala.quarta
          elif numDiaSemana == 3:
              diaSemana = user.escala.quinta
          elif numDiaSemana == 4:
              diaSemana = user.escala.sexta
          elif numDiaSemana == 5:
              diaSemana = user.escala.sabado
          elif numDiaSemana == 6:
              diaSemana = user.escala.domingo  
          if diaSemana:
            HistRegistro.objects.create(userReg_id = user.id, escala_id = user.escala.id, dataReg = (data.today().date() - timedelta(days=1)))    
   else:
      print('Tem feriado')   
   


def confereRegistros():
  # Ideia calcular apartir da escala a quantidade de horas trabalhadas se é maior ou igual, se for maior ou igual então aprova o registro direto se for menor então fica Pendente

  # Sempre verificar a primeira e a ultima saida se existe o registro, e o registro deve existir se existir na escala
  print('Registros')



def teste():
   print((data.today().date() - timedelta(days=1)))   
