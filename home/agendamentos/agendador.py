from home.models import Feriado, HistRegistro, Escala
from accounts.models import Users
from datetime import datetime as hora, datetime as data, timedelta
from decouple import config
import requests


def teste():
    print('ola')


# def get_api_feriados():
#   resposta = requests.get(f'https://api.invertexto.com/v1/holidays/2023?token={config("TOKEN")}&state=SC')
#   if resposta.status_code == 200:
#       json = resposta.json()
#       if json:
#           print(json)
#           for feriado in json:
              
#               if feriado['type'] == 'facultativo':
#                 tipo = 1

#               elif feriado['type'] == 'feriado':
#                 tipo = 2

#               if feriado['level'] == 'nacional':   
#                 level = 1

#               Feriado.objects.create(data= feriado['date'], nome=feriado['name'], tipo_id = tipo, level_id = level)
  
#   else:
#       print('Deu B.O')        


# def gera_escala_zerada():
   
