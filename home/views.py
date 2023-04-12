from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import HistRegistro, HoraExtra
import calendar
from datetime import datetime as hora, datetime as data, timedelta, time
from django.contrib import messages


@login_required
def RegistrarPonto(request):
    context = {}
    context['dataHoje'] = data.today().strftime("%d / %B")
    context['diaSemana'] = calendar.day_name[data.today().weekday()].capitalize()
    user = request.user
    if HistRegistro.objects.filter(userReg_id = user.id,  escala_id = user.escala.id, dataReg = data.today().date()):
        context['histRegistro'] = HistRegistro.objects.get(userReg = user.id,  escala_id = user.escala.id, dataReg = data.today().date())
    if HoraExtra.objects.filter(userExtra_id = user.id, dataExtra = data.today().date()):
        context['horaExtra'] = HoraExtra.objects.get(userExtra_id = user.id, dataExtra = data.today().date())    

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

    context['extraSemana'] = diaSemana

    if request.method == 'POST':
        ha = hora.now().time()
        if diaSemana == True:
            messages.error(request, 'Está na escala semanal correta!!')  
            print('Está na escala semanal correta!!')  
            
            if user.escala.horEnt1 is not None:
                horaEnt1_soma = (hora.combine(hora.today(), user.escala.horEnt1) + timedelta(minutes=5)).time()
                horaEnt1_subtrai = (hora.combine(hora.today(), user.escala.horEnt1) + timedelta(minutes=-5)).time()

            if user.escala.horSai2 is not None:
                horaSai2_soma = (hora.combine(hora.today(), user.escala.horSai2) + timedelta(minutes=5)).time()
                horaSai2_subtrai = (hora.combine(hora.today(), user.escala.horSai2) + timedelta(minutes=-5)).time()

            if user.escala.horEnt3 is not None:
                horaEnt3_soma = (hora.combine(hora.today(), user.escala.horEnt3) + timedelta(minutes=5)).time()
                horaEnt3_subtrai = (hora.combine(hora.today(), user.escala.horEnt3) + timedelta(minutes=-5)).time()
            
            # if user.escala.horSai4 != '':
            #     horaSai4_soma = (hora.combine(hora.today(), user.escala.horSai4) + timedelta(minutes=5)).time()
            #     horaSai4_subtrai = (hora.combine(hora.today(), user.escala.horSai4) + timedelta(minutes=-5)).time()
            
            print((horaEnt1_subtrai <= ha) and (horaSai2_subtrai > ha))
            print(f'hora {horaEnt1_subtrai} é menor ou igual a hora atual e a hora de saida {horaSai2_subtrai} é maior que a hora atual')
            # print((horaSai2_subtrai  <= ha) and (horaEnt3_subtrai > ha))
            # print(f'hora {horaSai2_subtrai} é menor ou igual a hora atual e a hora de saida {horaEnt3_subtrai} é maior que a hora atual')
            # # print((horaEnt3_subtrai <= ha) and (horaSai4_subtrai > ha))
            # print(f'hora {horaEnt3_subtrai} é menor ou igual a hora atual e a hora de saida {horaSai4_subtrai} é maior que a hora atual')
            # print((horaSai4_subtrai <= ha))
            # print(f'hora {horaSai4_subtrai} é menor ou igual a hora atual')

            temRegHistorico = HistRegistro.objects.filter(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date())    
            # Verifica se o usuario tem registro
            if not temRegHistorico:
                    HistRegistro.objects.create(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date(), horEnt1=ha) 


                    #Validação para adicionar dados ao banco de horas
                    altHist = HistRegistro.objects.get(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date())
                    horPercorridas =  hora.combine(hora.today(), user.escala.horEnt1) - hora.combine(hora.today(), ha) 
                    if (hora.combine(hora.today(), ha) < hora.combine(hora.today(), horaEnt1_subtrai)):
                        print('É menor que o horario padrão Então Saldo Negativo')
                        horPercorridas =  hora.combine(hora.today(), user.escala.horEnt1) - hora.combine(hora.today(), ha) 
                        min_f = horPercorridas.seconds// 60


                        resultado =  time(hour=min_f // 60, minute=min_f % 60)
                        print(time(hour=min_f // 60))
                        print(time(minute=min_f % 60))
                        print(resultado)

                        altHist.bancoHora = resultado
                        altHist.save()
                    elif (hora.combine(hora.today(), horaEnt1_soma) < hora.combine(hora.today(), ha)):
                        print('É maior que o horario padrão Então Saldo Negativo')
                        horPercorridas =  hora.combine(hora.today(), ha) - hora.combine(hora.today(), user.escala.horEnt1) 
                        min_f = horPercorridas.seconds// 60


                        resultado =  time(hour=min_f // 60, minute=min_f % 60)
                        print(time(hour=min_f // 60))
                        print(time(minute=min_f % 60))
                        print(resultado)

                        altHist.bancoHora = resultado # Precisa adicionar função para colocar horas negativas!!
                        altHist.save()

                        altHist.save()   
                    
                    
                    return render(request, 'registraPonto/index.html', context) 
                
            else:
                altHist = HistRegistro.objects.get(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date())
                print(altHist.horEnt3)
                if altHist.horSai2 is None: 
                    altHist.horSai2 = ha
                    altHist.save()   
                    return render(request, 'registraPonto/index.html', context) 

                elif altHist.horEnt3 is None: 
                    if ((hora.combine(hora.today(), ha) - hora.combine(hora.today(), altHist.horSai2)) >= timedelta(minutes=30)):
                            print('Faz mais de 30 minutos que registrou o ultimo ponto no sistema')
                            altHist.horEnt3 = ha
                            altHist.save()   
                            return render(request, 'registraPonto/index.html', context) 
                            
                    else:
                        horPercorridas = str(hora.combine(hora.today(), ha) - hora.combine(hora.today(), altHist.horSai2))
                        messages.error(request, f"Você precisa aguardar ao minimo 30 minutos para registrar o ponto novamente! Se passaram {horPercorridas[:-6]} desde o ulimo registro" )
                        print(type(hora.combine(hora.today(), ha) - hora.combine(hora.today(), altHist.horSai2)))
                        return render(request, 'registraPonto/index.html', context) 

                
                elif altHist.horSai4 is None: 
                    altHist.horSai4 = ha
                    altHist.save()  
                    return render(request, 'registraPonto/index.html', context)  

                else:
                    if not HoraExtra.objects.filter(userExtra_id = user.id, dataExtra=data.today().date()):
                        HoraExtra.objects.create(userExtra_id = user.id, dataExtra=data.today().date(), horEnt1=ha) 
                        return render(request, 'registraPonto/index.html', context)
                    else:
                        horExtra = HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date())     
                        if horExtra.horSai2 is None:
                            horExtra.horSai2 = ha
                            horExtra.save()
                            return render(request, 'registraPonto/index.html', context)
                        if horExtra.horEnt3 is None:
                            horExtra.horEnt3 = ha
                            horExtra.save()
                            return render(request, 'registraPonto/index.html', context)
                        if horExtra.horSai4 is None:
                            horExtra.horSai4 = ha
                            horExtra.save()
                            return render(request, 'registraPonto/index.html', context)
            
            #    messages.error(request, "Você está fora da sua escala de trabalho!")
            #    return render(request, 'registraPonto/index.html', context) 
        else:
            if not HoraExtra.objects.filter(userExtra_id = user.id, dataExtra=data.today().date()):
                        HoraExtra.objects.create(userExtra_id = user.id, dataExtra=data.today().date(), horEnt1=ha)
                        messages.error(request, "Hora Extra Registrada!") 
                        return render(request, 'registraPonto/index.html', context)
            else:
                horExtra = HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date())     
                if horExtra.horSai2 is None:
                    horExtra.horSai2 = ha
                    horExtra.save()
                    messages.error(request, "Hora Extra Registrada!") 
                    return render(request, 'registraPonto/index.html', context)
                if horExtra.horEnt3 is None:
                    horExtra.horEnt3 = ha
                    horExtra.save()
                    return render(request, 'registraPonto/index.html', context)
                if horExtra.horSai4 is None:
                    horExtra.horSai4 = ha
                    horExtra.save()
                    return render(request, 'registraPonto/index.html', context)
                

            messages.error(request, 'Não está na escala da semana correta!!') 
        return render(request, 'registraPonto/index.html', context)     
    else:    
        return render(request, 'registraPonto/index.html', context)
