from home.models import Feriado, HistRegistro, Escala
from accounts.models import Users
from datetime import datetime as hora, datetime as data, timedelta
from django.db.models import Q
from decouple import config
import requests
import os

from processos.processos import enviaEmailDivReg 

global cont
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
        print(user)
        print(HistRegistro.objects.filter(userReg_id = user.id, dataReg = (data.today().date() - timedelta(days=1))).exists())
        if not HistRegistro.objects.filter(userReg_id = user.id, dataReg = (data.today().date() - timedelta(days=1))).exists():
          print('Não tem Registro')
          numDiaSemana = (data.today().date() - timedelta(days=1)).weekday()

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
          print(diaSemana)    
          if diaSemana:
            HistRegistro.objects.create(userReg_id = user.id, escala_id = user.escala.id, dataReg = (data.today().date() - timedelta(days=1)))    
          print('\n')  
   else:
      print('Tem feriado')   
   


def confereRegistros():
  print('Entrei a primeira vez aqui ó')
  numDiaSemana = (data.today().date() - timedelta(days=1)).weekday()
  for user in Users.objects.filter(dat_inicia_trab__lte=(data.today().date() - timedelta(days=1)), is_active = True):
    print(user)
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
      reg = HistRegistro.objects.get(userReg_id = user.id, dataReg = (data.today().date() - timedelta(days=1)), sitAPR = 'PEN')
      #Verifica se tem o ultimo periodo cadastrado na escala do usuarioa 
      if user.escala.horSai4 is not None:

        if (reg.horEnt1 is not None) and (reg.horSai2 is not None) and (reg.horEnt3 is not None) and (reg.horSai4 is not None):
          escalaHor1Peri = hora.combine(hora.today(),  user.escala.horSai2) - hora.combine(hora.today(), user.escala.horEnt1)
          escalaHor2Peri = hora.combine(hora.today(),  user.escala.horSai4) - hora.combine(hora.today(), user.escala.horEnt3)
          horEscala = (escalaHor1Peri + escalaHor2Peri)
          #Remove 10 minutos para seguir Regra da CLT dos minutos diarios 
          horEscala = horEscala  + timedelta(minutes=-10)

          RegHor1Peri = hora.combine(hora.today(), reg.horSai2) - hora.combine(hora.today(), reg.horEnt1)
          RegHor2Peri = hora.combine(hora.today(),  reg.horSai4) - hora.combine(hora.today(), reg.horEnt3)
          horRegistro = RegHor1Peri + RegHor2Peri
          if horEscala <= horRegistro:
            reg.sitAPR = 'APR'
            reg.save()
            print('Pronto aprovado automaticamente')
          else:
             enviaEmailDivReg(user.email, {'registro': reg})
             print('Envia e-mail informando que ficou faltando uma quantidade X de horas')

          print('escala com mais de 1 periodo')
        else:
           enviaEmailDivReg(user.email, {'registro': reg})
           print('Envia e-mail informando a falta de um registro')  
      else:
        print('escala para usuario de apenas 1 periodo')  
        if (reg.horEnt1 is not None) and (reg.horSai2 is not None):
          horEscala = hora.combine(hora.today(),  user.escala.horSai2) - hora.combine(hora.today(), user.escala.horEnt1)
          #Remove 10 minutos para seguir Regra da CLT dos minutos diarios 
          horEscala = horEscala + timedelta(minutes=-10)
          horRegistro = hora.combine(hora.today(), reg.horSai2) - hora.combine(hora.today(), reg.horEnt1)
          if horEscala <= horRegistro:
              reg.sitAPR = 'APR'
              reg.save()
              print('Pronto aprovado automaticamente')
          else:
              enviaEmailDivReg(user.email, {'registro': reg})
              print('Envia e-mail informando que ficou faltando uma quantidade X de horas')
        else:
            enviaEmailDivReg(user.email, {'registro': reg})
            print('Envia e-mail informando que ficou sem registrar a saida')

    else:
       print('Fora da Escala')   
    print('\n')
   

def remov_Process_started():
   # Remove o arquivo process_started.txt, se existir
  if os.path.isfile('process_started.txt'):
    os.remove('process_started.txt')