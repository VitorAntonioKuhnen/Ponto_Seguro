from home.models import Feriado, HistRegistro, Escala
from accounts.models import Users
from datetime import datetime as hora, datetime as data, timedelta
from django.db.models import Q
from decouple import config
import requests


def teste():
    print('ola')

def test2():
    print('novo teste')

def get_api_feriados():
  resposta = requests.get(f'https://api.invertexto.com/v1/holidays/2023?token={config("TOKEN")}&state=SC')
  if resposta.status_code == 200:
      json = resposta.json()
      if json:
          print(json)
          for feriado in json:
              
              if feriado['type'] == 'facultativo':
                tipo = 1

              elif feriado['type'] == 'feriado':
                tipo = 2

              if feriado['level'] == 'nacional':   
                level = 1

              Feriado.objects.create(data= feriado['date'], nome=feriado['name'], tipo_id = tipo, level_id = level)
  
  else:
      print('Deu B.O')        


def gera_escala_zerada():
   feriado = Feriado.objects.filter(data = data.now())
   if not feriado:
      print('entrou')
      print(Users.objects.filter(Q(dat_inicia_trab__gte=data.today().date()), is_active = True))
      for user in Users.objects.filter( is_active = True):
        print(user)
        print(HistRegistro.objects.filter(userReg_id = user.id, dataReg = data.today().date()))
        

      # numDiaSemana = data.today().weekday()
      # if numDiaSemana == 0:
      #     diaSemana = Users.escala.segunda
      # elif numDiaSemana == 1:
      #     diaSemana = Users.escala.terca
      # elif numDiaSemana == 2:
      #     diaSemana = Users.escala.quarta
      # elif numDiaSemana == 3:
      #     diaSemana = Users.escala.quinta
      # elif numDiaSemana == 4:
      #     diaSemana = Users.escala.sexta
      # elif numDiaSemana == 5:
      #     diaSemana = Users.escala.sabado
      # elif numDiaSemana == 6:
      #     diaSemana = Users.escala.domingo  
    

      #Aqui fazer a logica para executar o processo de criação de escalas quando não se trata de um feriado
      print('Não tem feriado')  
   else:
      print('Tem feriado')   
   
