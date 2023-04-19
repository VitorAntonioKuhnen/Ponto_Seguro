from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import HistRegistro, HoraExtra
import calendar
from datetime import datetime as hora, datetime as data, timedelta, time
from django.utils import timezone
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
            
            if user.escala.horSai4 is not None:
                horaSai4_soma = (hora.combine(hora.today(), user.escala.horSai4) + timedelta(minutes=5)).time()
                horaSai4_subtrai = (hora.combine(hora.today(), user.escala.horSai4) + timedelta(minutes=-5)).time()
            
        
            temRegHistorico = HistRegistro.objects.filter(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date())    
            # Verifica se o usuario tem registro de histórico de escala
            if not temRegHistorico:
                    HistRegistro.objects.create(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date(), horEnt1=ha) 


                    #Validação para adicionar dados ao banco de horas
                    altHist = HistRegistro.objects.get(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date())
                    horPercorridas =  hora.combine(hora.today(), user.escala.horEnt1) - hora.combine(hora.today(), ha) 
                    if (hora.combine(hora.today(), ha) < hora.combine(hora.today(), horaEnt1_subtrai)):
                        print('É menor que o horario da escala Então Saldo é positivo')
                        horPercorridas =  hora.combine(hora.today(), user.escala.horEnt1) - hora.combine(hora.today(), ha) 
                        print(horPercorridas.seconds// 60)
                        altHist.bancoHoraMin = horPercorridas.seconds// 60
                        altHist.save()

                    elif (hora.combine(hora.today(), horaEnt1_soma) < hora.combine(hora.today(), ha)):
                        print('É maior que o horario da escala Então Saldo Negativo')
                        horPercorridas =  hora.combine(hora.today(), ha) - hora.combine(hora.today(), user.escala.horEnt1) 
                        print(-(horPercorridas.seconds// 60))
                        altHist.bancoHoraMin = -(horPercorridas.seconds// 60)
                        altHist.save() 
                    
                    
                    # return render(request, 'registraPonto/index.html', context) 
                    return redirect(inicio) 
            #Segundo registro da Escala    
            else:
                altHist = HistRegistro.objects.get(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date())
                if altHist.horSai2 is None: 
                    altHist.horSai2 = ha

                    if (hora.combine(hora.today(), horaSai2_subtrai) > hora.combine(hora.today(), ha)):
                        print('É menor que o horario atual Então Saldo Negativo')

                        horPercorridas =  hora.combine(hora.today(), user.escala.horSai2) - hora.combine(hora.today(), ha)
                        print(horPercorridas) 
                        print(horPercorridas.seconds// 60)
                        print(altHist.bancoHoraMin)
                        

                        if (altHist.bancoHoraMin < 0 ):
                            altHist.bancoHoraMin = altHist.bancoHoraMin +  (-(horPercorridas.seconds// 60))
                        else:
                            altHist.bancoHoraMin = (-(horPercorridas.seconds// 60)) + altHist.bancoHoraMin    

                    elif (hora.combine(hora.today(), horaSai2_soma) < hora.combine(hora.today(), ha)):
                        print('É maior que o horario padrão Então Saldo Positivo')

                        horPercorridas = hora.combine(hora.today(), ha) - hora.combine(hora.today(), user.escala.horSai2)

                        if (altHist.bancoHoraMin < 0 ):
                            altHist.bancoHoraMin =  altHist.bancoHoraMin + (horPercorridas.seconds// 60)
                        else:
                            altHist.bancoHoraMin = (horPercorridas.seconds// 60) + altHist.bancoHoraMin    

                    altHist.save()   
                    
                    # return render(request, 'registraPonto/index.html', context) 
                    return redirect(inicio)
                #Terceiro registro da Escala
                elif altHist.horEnt3 is None: 
                    if ((hora.combine(hora.today(), ha) - hora.combine(hora.today(), altHist.horSai2)) >= timedelta(minutes=30)):
                            print('Faz mais de 30 minutos que registrou o ultimo ponto no sistema')
                            altHist.horEnt3 = ha

                            if (hora.combine(hora.today(), ha) < hora.combine(hora.today(), horaEnt3_subtrai)):
                                print('É menor que o horario padrão Então Saldo Positivo')

                                horPercorridas =  hora.combine(hora.today(), user.escala.horEnt3) - hora.combine(hora.today(), ha)
                                print(horPercorridas) 
                                print(horPercorridas.seconds// 60)
                                print(altHist.bancoHoraMin)
                                
                                if (altHist.bancoHoraMin < 0 ):
                                    print(altHist.bancoHoraMin)

                                    altHist.bancoHoraMin =  altHist.bancoHoraMin + (horPercorridas.seconds// 60)

                                    print((-(horPercorridas.seconds// 60)))
                                    print(altHist.bancoHoraMin +  (-(horPercorridas.seconds// 60)))
                                    print((-(horPercorridas.seconds// 60)) + altHist.bancoHoraMin)
                                else:
                                    altHist.bancoHoraMin = (horPercorridas.seconds// 60) + altHist.bancoHoraMin    


                            elif (hora.combine(hora.today(), horaSai2_soma) < hora.combine(hora.today(), ha)):
                                print('É maior que o horario padrão Então Saldo Negativo')

                                horPercorridas = hora.combine(hora.today(), ha) - hora.combine(hora.today(), user.escala.horEnt3)

                                if (altHist.bancoHoraMin > 0 ):
                                    altHist.bancoHoraMin = altHist.bancoHoraMin +  (-(horPercorridas.seconds// 60))
                                else:
                                    altHist.bancoHoraMin = (-(horPercorridas.seconds// 60)) + altHist.bancoHoraMin

                            altHist.save()   
                            # return render(request, 'registraPonto/index.html', context)
                            return redirect(inicio) 
                            
                    else:
                        horPercorridas = str(hora.combine(hora.today(), ha) - hora.combine(hora.today(), altHist.horSai2))
                        messages.error(request, f"Você precisa aguardar ao minimo 30 minutos para registrar o ponto novamente! Se passaram {horPercorridas[:-6]} desde o ulimo registro" )
                        print(type(hora.combine(hora.today(), ha) - hora.combine(hora.today(), altHist.horSai2)))
                        # return render(request, 'registraPonto/index.html', context) 
                        return redirect(inicio)

                #Ultimo registro da Escala
                elif altHist.horSai4 is None: 
                    altHist.horSai4 = ha 

                    if (hora.combine(hora.today(), horaSai4_subtrai) > hora.combine(hora.today(), ha)):
                        print('É menor que o horario atual Então Saldo Negativo')

                        horPercorridas =  hora.combine(hora.today(), user.escala.horSai4) - hora.combine(hora.today(), ha)
                        print(horPercorridas) 
                        print(horPercorridas.seconds// 60)
                        print(altHist.bancoHoraMin)
                        

                        if (altHist.bancoHoraMin < 0 ):
                            altHist.bancoHoraMin = altHist.bancoHoraMin +  (-(horPercorridas.seconds// 60))
                        else:
                            altHist.bancoHoraMin = (-(horPercorridas.seconds// 60)) + altHist.bancoHoraMin    

                    elif (hora.combine(hora.today(), horaSai4_soma) < hora.combine(hora.today(), ha)):
                        print('É maior que o horario padrão Então Saldo Positivo')

                        horPercorridas = hora.combine(hora.today(), ha) - hora.combine(hora.today(), user.escala.horSai4)

                        if (altHist.bancoHoraMin < 0 ):
                            altHist.bancoHoraMin =  altHist.bancoHoraMin + (horPercorridas.seconds// 60)
                        else:
                            altHist.bancoHoraMin = (horPercorridas.seconds// 60) + altHist.bancoHoraMin    
                    altHist.save()  
                    # return render(request, 'registraPonto/index.html', context)  
                    return redirect(inicio)

                else:
                    if not HoraExtra.objects.filter(userExtra_id = user.id, dataExtra=data.today().date()):
                        HoraExtra.objects.create(userExtra_id = user.id, dataExtra=data.today().date(), horEnt1=ha) 
                        # return render(request, 'registraPonto/index.html', context)
                        return redirect(inicio)
                    else:
                        horExtra = HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date())     
                        if horExtra.horSai2 is None:
                            horExtra.horSai2 = ha
                            horExtra.save()
                            # return render(request, 'registraPonto/index.html', context)
                        if horExtra.horEnt3 is None:
                            horExtra.horEnt3 = ha
                            horExtra.save()
                            # return render(request, 'registraPonto/index.html', context)
                        if horExtra.horSai4 is None:
                            horExtra.horSai4 = ha
                            horExtra.save()
                            # return render(request, 'registraPonto/index.html', context)   
                        return redirect(inicio)    
            
            #    messages.error(request, "Você está fora da sua escala de trabalho!")
            #    return render(request, 'registraPonto/index.html', context) 
        else:
            if not HoraExtra.objects.filter(userExtra_id = user.id, dataExtra=data.today().date()):
                        HoraExtra.objects.create(userExtra_id = user.id, dataExtra=data.today().date(), horEnt1=ha)
                        messages.error(request, "Hora Extra Registrada!") 
                        # return render(request, 'registraPonto/index.html', context)
                        return redirect(inicio)
            else:
                horExtra = HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date())     
                if horExtra.horSai2 is None:
                    horExtra.horSai2 = ha
                    horExtra.save()
                    messages.error(request, "Hora Extra Registrada!") 
                    # return render(request, 'registraPonto/index.html', context)
                if horExtra.horEnt3 is None:
                    horExtra.horEnt3 = ha
                    horExtra.save()
                    # return render(request, 'registraPonto/index.html', context)
                if horExtra.horSai4 is None:
                    horExtra.horSai4 = ha
                    horExtra.save()
                    # return render(request, 'registraPonto/index.html', context)
                return redirect(inicio)    
                

            messages.error(request, 'Não está na escala da semana correta!!') 
        # return render(request, 'registraPonto/index.html', context)     
    else:    
        return render(request, 'registraPonto/index.html', context)

@login_required
def inicio(request):
    return render(request, 'home/index.html')