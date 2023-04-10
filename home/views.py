from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import HistRegistro
from accounts.models import Users
import calendar
# import datetime as data
from django.utils import timezone
from datetime import datetime as hora, datetime as data, timedelta
from django.contrib import messages


@login_required
def RegistrarPonto(request):
    context = {}
    context['dataHoje'] = data.today().strftime("%d / %B")
    context['diaSemana'] = calendar.day_name[data.today().weekday()].capitalize()
    user = request.user
    if HistRegistro.objects.filter(userReg = user.id,  escala_id = user.escala.id, dataReg = data.today().date()):
        context['histRegistro'] = HistRegistro.objects.get(userReg = user.id,  escala_id = user.escala.id, dataReg = data.today().date())

    if request.method == 'POST':
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

        if diaSemana == True:
            messages.error(request, 'Está na escala semanal correta!!')  
            print('Está na escala semanal correta!!')  

            ha = hora.now().time()
            horaEnt1_soma = (hora.combine(hora.today(), user.escala.horEnt1) + timedelta(minutes=5)).time()
            horaEnt1_subtrai = (hora.combine(hora.today(), user.escala.horEnt1) + timedelta(minutes=-5)).time()

            horaSai2_soma = (hora.combine(hora.today(), user.escala.horSai2) + timedelta(minutes=5)).time()
            horaSai2_subtrai = (hora.combine(hora.today(), user.escala.horSai2) + timedelta(minutes=-5)).time()

            horaEnt3_soma = (hora.combine(hora.today(), user.escala.horEnt3) + timedelta(minutes=5)).time()
            horaEnt3_subtrai = (hora.combine(hora.today(), user.escala.horEnt3) + timedelta(minutes=-5)).time()

            horaSai4_soma = (hora.combine(hora.today(), user.escala.horSai4) + timedelta(minutes=5)).time()
            horaSai4_subtrai = (hora.combine(hora.today(), user.escala.horSai4) + timedelta(minutes=-5)).time()
            
            print((horaEnt1_subtrai <= ha) and (horaSai2_subtrai > ha))
            print(f'hora {horaEnt1_subtrai} é menor ou igual a hora atual e a hora de saida {horaSai2_subtrai} é maior que a hora atual')
            print((horaSai2_subtrai  <= ha) and (horaEnt3_subtrai > ha))
            print(f'hora {horaSai2_subtrai} é menor ou igual a hora atual e a hora de saida {horaEnt3_subtrai} é maior que a hora atual')
            print((horaEnt3_subtrai <= ha) and (horaSai4_subtrai > ha))
            print(f'hora {horaEnt3_subtrai} é menor ou igual a hora atual e a hora de saida {horaSai4_subtrai} é maior que a hora atual')
            print((horaSai4_subtrai <= ha))
            print(f'hora {horaSai4_subtrai} é menor ou igual a hora atual')

            temRegHistorico = HistRegistro.objects.filter(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date())    
            # Verifica se o usuario está dentro da sua escala
            if ((horaEnt1_subtrai <= ha) and (horaSai2_subtrai > ha)):
                print('Primeiro horario')   
                if not temRegHistorico:
                    HistRegistro.objects.create(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date(), horEnt1=ha)
                else:
                    altHist = HistRegistro.objects.get(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date())

                    altHist.horSai2 = ha
                    altHist.save()   

            elif ((horaSai2_subtrai  <= ha) and (horaEnt3_subtrai > ha)):
                print('Segundo horario') 
                if not temRegHistorico:
                    HistRegistro.objects.create(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date(), horSai2=ha)
                else:
                    altHist = HistRegistro.objects.get(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date())
                    altHist.horSai2 = ha
                    altHist.save()   


            elif ((horaEnt3_subtrai <= ha) and (horaSai4_subtrai > ha)):
                print('Terceiro horario')  
                if not temRegHistorico:
                    HistRegistro.objects.create(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date(), horEnt3=ha)
                else:
                    altHist = HistRegistro.objects.get(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date())

                    if ((hora.combine(hora.today(), ha) - hora.combine(hora.today(), altHist.horSai2)) >= timedelta(minutes=30)):
                        print('Faz mais de 30 minutos que registrou o ultimo ponto no sistema')
                        altHist.horEnt3 = ha
                        altHist.save()   
                        
                    else:
                        horPercorridas = str(hora.combine(hora.today(), ha) - hora.combine(hora.today(), altHist.horSai2))
                        messages.error(request, f"Você precisa aguardar ao minimo 30 minutos para registrar o ponto novamente! Se passaram {horPercorridas[:-6]} desde o ulimo registro" )
                    #     print(hora.combine(hora.today(), ha) - hora.combine(hora.today(), altHist.horSai2))
                    # print(hora.combine(hora.today(), ha) - hora.combine(hora.today(), altHist.horSai2))

            elif (horaSai4_subtrai <= ha):
                print('Quarto horario')   

                if not temRegHistorico:
                    HistRegistro.objects.create(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date(), horSai4=ha)
                else:
                    altHist = HistRegistro.objects.get(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date())
                    print(altHist.dataReg)
                    print(data.today().date())
                    altHist.horSai4 = ha
                    altHist.save()  


                print(type(horaSai4_subtrai))  
                print(type(ha))  
                # Se estiver então verificda se já possui registro
                if HistRegistro.objects.filter(userReg = user.id, escala = user.escala.id, dataReg = data.today()):

                    if not (horaEnt1_soma >= ha) and (horaEnt1_subtrai  <= ha):
                        messages.error(request, "Você não pode registrar o ponto")
                        
                    print(user.escala.id) 
                    print(request.POST.get('horas'))
                    # messages.error(request, "Problemas ao registrar ponto")  
                    return render(request, 'registraPonto/index.html', context)
                # else:
                #     if user.escala.horaEntM != '':
                #         #  Se o usuario tentar entrar 5 minutos antes do seu horario e até 5 minutos depois ele consegue
                #         # Escala de entrada 08:00 - 5 = 07:55 for maior ou igual ao horario atual e a escala de entrada 08:00 + 5 = 08:05 for menor ou igual a hora atual ele cria o registro 
                #         if (horaEnt1_subtrai  >= ha) and (horaEnt1_soma <= ha):
                #             HistRegistro.objects.create(userReg = user.id, escala = user.escala.id, dataReg = data.date.today(), horaEntM = ha)
                #         elif (horaSai2_subtrai  >= ha) and (horaSai2_soma <= ha):
                #             HistRegistro.objects.create(userReg = user.id, escala = user.escala.id, dataReg = data.date.today(), horaSaiM = ha)
                #     else:
                #         HistRegistro.objects.create(userReg = user.id, escala = user.escala.id, dataReg = data.date.today(), horaEntV = ha)     
            else:
               messages.error(request, "Você está fora da sua escala de trabalho!")
               return render(request, 'registraPonto/index.html', context) 
        else:
            messages.error(request, 'Não está na escala da semana correta!!') 
        return render(request, 'registraPonto/index.html', context)     
    else:    
        return render(request, 'registraPonto/index.html', context)
