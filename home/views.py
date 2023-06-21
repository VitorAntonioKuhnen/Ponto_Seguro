from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import HistRegistro, HoraExtra, TipoJustificativa, Escala, Feriado
from accounts.models import Users, Cargo
import calendar
from datetime import datetime as hora, datetime as data, timedelta
from django.utils.dateparse import parse_time
from django.contrib import messages, auth
from django.http import HttpResponse, JsonResponse
from accounts import views
from django.db.models import Q, F, ExpressionWrapper, DateTimeField

import json
from django.core.serializers import serialize


#Paginação Django
from django.core.paginator import Paginator

#Arquivo com processos 
from processos import processos


@login_required
def RegistrarPonto(request):
    context = {}
    context['dataHoje'] = data.today().strftime("%d / %B")
    context['diaSemana'] = calendar.day_name[data.today().weekday()].capitalize()
    user = request.user

    #Verifica se é feriado para atualizar a informação do registro na tela
    if Feriado.objects.filter(data = data.now()):
       context['feriado'] = False  
    else:
       context['feriado'] = True

    RegMeioPeriodo = False
    if HistRegistro.objects.filter(userReg_id = user.id,  escala_id = user.escala.id, dataReg = data.today().date()):
        context['histRegistro'] = HistRegistro.objects.get(userReg = user.id,  escala_id = user.escala.id, dataReg = data.today().date())
        if ((HistRegistro.objects.get(userReg = user.id,  escala_id = user.escala.id, dataReg = data.today().date()).horSai2 != None and user.escala.horSai4 == None)):
            context['feriado'] = False
            RegMeioPeriodo = True

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
            print('Está na escala semanal correta!!')  
            if (not Feriado.objects.filter(data = data.now()) and (not RegMeioPeriodo)):
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
                        HistRegistro.objects.create(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date(), horEnt1=ha.strftime('%H:%M')) 


                        #Validação para adicionar dados ao banco de horas
                        altHist = HistRegistro.objects.get(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date())
                        horPercorridas =  hora.combine(hora.today(), user.escala.horEnt1) - hora.combine(hora.today(), ha) 
                        if (hora.combine(hora.today(), ha) < hora.combine(hora.today(), horaEnt1_subtrai)):
                            print('É menor que o horario da escala Então Saldo é positivo')
                            # horPercorridas =  hora.combine(hora.today(), user.escala.horEnt1) - hora.combine(hora.today(), ha) 
                            # print(horPercorridas.seconds// 60)
                            # altHist.bancoHoraMin = horPercorridas.seconds// 60

                        elif (hora.combine(hora.today(), horaEnt1_soma) < hora.combine(hora.today(), ha)):
                            print('É maior que o horario da escala Então Saldo Negativo')
                            # horPercorridas =  hora.combine(hora.today(), ha) - hora.combine(hora.today(), user.escala.horEnt1) 
                            # print(-(horPercorridas.seconds// 60))

                            user.justificar = True
                            user.save()

                            # altHist.bancoHoraMin = -(horPercorridas.seconds// 60)
                            
                        
                        
                        altHist.save() 
                        messages.success(request, f'Primeira Entrada Registrada com Sucesso {str(altHist.horEnt1)[:-6]}') 
                        return redirect(inicio)
                
                #Segundo registro da Escala    
                else:
                    altHist = HistRegistro.objects.get(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date())
                    if altHist.horSai2 is None: 
                        altHist.horSai2 = ha.strftime('%H:%M')

                        if (hora.combine(hora.today(), horaSai2_subtrai) < hora.combine(hora.today(), ha)):
                            print('Escala é menor que o horario atual Então Saldo Negativo')

                            # horPercorridas =  hora.combine(hora.today(), user.escala.horSai2) - hora.combine(hora.today(), ha)
                            # print(horPercorridas) 
                            # print(horPercorridas.seconds// 60)
                            # print(altHist.bancoHoraMin)
                            
                            # user.justificar = True
                            # user.save()

                            # if (altHist.bancoHoraMin < 0 ):
                            #     altHist.bancoHoraMin = altHist.bancoHoraMin +  (-(horPercorridas.seconds// 60))
                            # else:
                            #     altHist.bancoHoraMin = (-(horPercorridas.seconds// 60)) + altHist.bancoHoraMin    

                        elif (hora.combine(hora.today(), horaSai2_soma) > hora.combine(hora.today(), ha)):
                            print('Escala é maior que o horario atual Então Saldo Positivo')

                            # horPercorridas = hora.combine(hora.today(), ha) - hora.combine(hora.today(), user.escala.horSai2)

                            # if (altHist.bancoHoraMin < 0 ):
                            #     altHist.bancoHoraMin =  altHist.bancoHoraMin + (horPercorridas.seconds// 60)
                            # else:
                            #     altHist.bancoHoraMin = (horPercorridas.seconds// 60) + altHist.bancoHoraMin    
                        
                        altHist.save()   
                        messages.success(request, f'Segunda Saida Registrada com Sucesso {str(altHist.horSai2)[:-6]}')
                        auth.logout(request)
                        return redirect(views.login)
                    
                    #Terceiro registro da Escala
                    elif altHist.horEnt3 is None: 
                        if ((hora.combine(hora.today(), ha) - hora.combine(hora.today(), altHist.horSai2)) >= timedelta(minutes=30)):
                                print('Faz mais de 30 minutos que registrou o ultimo ponto no sistema')
                                altHist.horEnt3 = ha.strftime('%H:%M')

                                if (hora.combine(hora.today(), ha) < hora.combine(hora.today(), horaEnt3_subtrai)):
                                    print('É menor que o horario padrão Então Saldo Positivo')

                                    # horPercorridas =  hora.combine(hora.today(), user.escala.horEnt3) - hora.combine(hora.today(), ha)

                                    # print(horPercorridas) 
                                    # print(horPercorridas.seconds// 60)
                                    # print(altHist.bancoHoraMin)


                                    # if (altHist.bancoHoraMin < 0 ):
                                    #     print(altHist.bancoHoraMin)

                                    #     altHist.bancoHoraMin =  altHist.bancoHoraMin + (horPercorridas.seconds// 60)

                                    #     print((-(horPercorridas.seconds// 60))) 
                                    #     print(altHist.bancoHoraMin +  (-(horPercorridas.seconds// 60)))
                                    #     print((-(horPercorridas.seconds// 60)) + altHist.bancoHoraMin)
                                    # else:
                                    #     altHist.bancoHoraMin = (horPercorridas.seconds// 60) + altHist.bancoHoraMin    


                                elif (hora.combine(hora.today(), horaEnt3_soma) < hora.combine(hora.today(), ha)):
                                    print('É maior que o horario padrão Então Saldo Negativo')

                                    # horPercorridas = hora.combine(hora.today(), ha) - hora.combine(hora.today(), user.escala.horEnt3)
                                    
                                    user.justificar = True
                                    user.save()

                                    # if (altHist.bancoHoraMin > 0 ):
                                    #     altHist.bancoHoraMin = altHist.bancoHoraMin +  (-(horPercorridas.seconds// 60))
                                    # else:
                                    #     altHist.bancoHoraMin = (-(horPercorridas.seconds// 60)) + altHist.bancoHoraMin

                                altHist.save()   

                                messages.success(request, f'Terceira Entrada Registrada com Sucesso {str(altHist.horEnt3)[:-6]}')
                                return redirect(inicio) 
                                
                        else:
                            horPercorridas = str(hora.combine(hora.today(), ha) - hora.combine(hora.today(), altHist.horSai2))
                            messages.error(request, f"Você precisa aguardar ao minimo 30 minutos para registrar o ponto novamente! Se passaram {horPercorridas[:-6]} desde o ulimo registro" )
                            print(type(hora.combine(hora.today(), ha) - hora.combine(hora.today(), altHist.horSai2)))
                            return render(request, 'registraPonto/index.html', context) 

                    #Ultimo registro da Escala
                    elif altHist.horSai4 is None: 
                        altHist.horSai4 = ha.strftime('%H:%M') 

                        if (hora.combine(hora.today(), horaSai4_subtrai) > hora.combine(hora.today(), ha)):
                            print('É menor que o horario atual Então Saldo Positivo')

                            # horPercorridas =  hora.combine(hora.today(), user.escala.horSai4) - hora.combine(hora.today(), ha)
                            # print(horPercorridas) 
                            # print(horPercorridas.seconds// 60)
                            # print(altHist.bancoHoraMin)

                            # user.justificar = True
                            # user.save()

                            # if (altHist.bancoHoraMin < 0 ):
                            #     altHist.bancoHoraMin = altHist.bancoHoraMin +  (-(horPercorridas.seconds// 60))
                            # else:
                            #     altHist.bancoHoraMin = (-(horPercorridas.seconds// 60)) + altHist.bancoHoraMin    

                        elif (hora.combine(hora.today(), horaSai4_soma) < hora.combine(hora.today(), ha)):
                            print('É maior que o horario padrão Então Saldo Negativo')

                            # horPercorridas = hora.combine(hora.today(), ha) - hora.combine(hora.today(), user.escala.horSai4)

                            # if (altHist.bancoHoraMin < 0 ):
                            #     altHist.bancoHoraMin =  altHist.bancoHoraMin + (horPercorridas.seconds// 60)
                            # else:
                            #     altHist.bancoHoraMin = (horPercorridas.seconds// 60) + altHist.bancoHoraMin    
                        altHist.save()  
                        messages.success(request, f'Quarta Saida Registrada com Sucesso {str(altHist.horSai4)[:-6]}') 
                        auth.logout(request)
                        return redirect(views.login)

                    else:
                        if not HoraExtra.objects.filter(userExtra_id = user.id, dataExtra=data.today().date()):
                            HoraExtra.objects.create(userExtra_id = user.id, dataExtra=data.today().date(), horEnt1=ha.strftime('%H:%M')) 
                            messages.success(request, f'Primeira Entrada Extra Registrada com Sucesso {str(HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date()).horEnt1)[:-6]}') 
                            user.justificar = True
                            user.save()
                            return redirect(inicio)
                        else:
                            horExtra = HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date())     
                            if horExtra.horSai2 is None:
                                horExtra.horSai2 = ha.strftime('%H:%M')
                                messages.success(request, f'Segunda Saida Extra Registrada com Sucesso {str(horExtra.horSai2)[:-6]}') 
                                horExtra.save()
                                auth.logout(request)
                                return redirect(views.login)
                            elif horExtra.horEnt3 is None:
                                if ((hora.combine(hora.today(), ha) - hora.combine(hora.today(), horExtra.horSai2)) >= timedelta(minutes=30)):
                                    horExtra.horEnt3 = ha.strftime('%H:%M')
                                    messages.success(request, f'Terceira Entrada Extra Registrada com Sucesso {str(horExtra.horSai2)[:-6]}') 
                                    horExtra.save()
                                    return redirect(inicio) 
                                else:
                                    horPercorridas = str(hora.combine(hora.today(), ha) - hora.combine(hora.today(), horExtra.horSai2))
                                    messages.error(request, f"Você precisa aguardar ao minimo 30 minutos para registrar o ponto novamente! Se passaram {horPercorridas[:-6]} desde o ulimo registro" )
                                    print(type(hora.combine(hora.today(), ha) - hora.combine(hora.today(), horExtra.horSai2)))
                                    return render(request, 'registraPonto/index.html', context)    
                            elif horExtra.horSai4 is None:
                                horExtra.horSai4 = ha.strftime('%H:%M')
                                messages.success(request, f'Quarta Saida Extra Registrada com Sucesso {str(horExtra.horSai2)[:-6]}') 
                                horExtra.save()
                                auth.logout(request)
                                return redirect(views.login)
            else:
                if not HoraExtra.objects.filter(userExtra_id = user.id, dataExtra=data.today().date()):
                            HoraExtra.objects.create(userExtra_id = user.id, dataExtra=data.today().date(), horEnt1=ha.strftime('%H:%M'))
                            messages.success(request, f'Primeira Entrada Extra Registrada com Sucesso {str(HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date()).horEnt1)}')
                            user.justificar = True
                            user.save()
                            return redirect(inicio)
                else:
                    horExtra = HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date())     
                    if horExtra.horSai2 is None:
                        horExtra.horSai2 = ha.strftime('%H:%M')
                        horExtra.save()
                        messages.success(request, f'Segunda Saida Extra Registrada com Sucesso {str(horExtra.horSai2)}') 
                        auth.logout(request)
                        return redirect(views.login)
                        
                    elif horExtra.horEnt3 is None:
                                if ((hora.combine(hora.today(), ha) - hora.combine(hora.today(), horExtra.horSai2)) >= timedelta(minutes=30)):
                                    horExtra.horEnt3 = ha.strftime('%H:%M')
                                    messages.success(request, f'Terceira Entrada Extra Registrada com Sucesso {str(horExtra.horSai2)[:-6]}') 
                                    horExtra.save()
                                    return redirect(inicio) 
                                else:
                                    horPercorridas = str(hora.combine(hora.today(), ha) - hora.combine(hora.today(), horExtra.horSai2))
                                    messages.error(request, f"Você precisa aguardar ao minimo 30 minutos para registrar o ponto novamente! Se passaram {horPercorridas[:-6]} desde o ulimo registro" )
                                    print(type(hora.combine(hora.today(), ha) - hora.combine(hora.today(), horExtra.horSai2)))
                                    return render(request, 'registraPonto/index.html', context)   
                        
                    elif horExtra.horSai4 is None:
                        horExtra.horSai4 = ha.strftime('%H:%M')
                        horExtra.save()
                        messages.success(request, f'Quarta Saida Extra Registrada com Sucesso {str(horExtra.horSai2)}')
                        auth.logout(request)
                        return redirect(views.login)
        else:
            if not HoraExtra.objects.filter(userExtra_id = user.id, dataExtra=data.today().date()):
                        HoraExtra.objects.create(userExtra_id = user.id, dataExtra=data.today().date(), horEnt1=ha.strftime('%H:%M'))
                        messages.success(request, f'Primeira Entrada Extra Registrada com Sucesso {str(HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date()).horEnt1)}')
                        user.justificar = True
                        user.save()
                        return redirect(inicio)
            else:
                horExtra = HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date())     
                if horExtra.horSai2 is None:
                    horExtra.horSai2 = ha.strftime('%H:%M')
                    horExtra.save()
                    messages.success(request, f'Segunda Saida Extra Registrada com Sucesso {str(horExtra.horSai2)}') 
                    auth.logout(request)
                    return redirect(views.login)
                    
                elif horExtra.horEnt3 is None:
                            if ((hora.combine(hora.today(), ha) - hora.combine(hora.today(), horExtra.horSai2)) >= timedelta(minutes=30)):
                                horExtra.horEnt3 = ha.strftime('%H:%M')
                                messages.success(request, f'Terceira Entrada Extra Registrada com Sucesso {str(horExtra.horSai2)[:-6]}') 
                                horExtra.save()
                                return redirect(inicio) 
                            else:
                                horPercorridas = str(hora.combine(hora.today(), ha) - hora.combine(hora.today(), horExtra.horSai2))
                                messages.error(request, f"Você precisa aguardar ao minimo 30 minutos para registrar o ponto novamente! Se passaram {horPercorridas[:-6]} desde o ulimo registro" )
                                print(type(hora.combine(hora.today(), ha) - hora.combine(hora.today(), horExtra.horSai2)))
                                return render(request, 'registraPonto/index.html', context)   
                    
                elif horExtra.horSai4 is None:
                    horExtra.horSai4 = ha.strftime('%H:%M')
                    horExtra.save()
                    messages.success(request, f'Quarta Saida Extra Registrada com Sucesso {str(horExtra.horSai2)}')
                    auth.logout(request)
                    return redirect(views.login)
                    
                   
               
    else:    
        return render(request, 'registraPonto/index.html', context)

@login_required
def inicio(request):
    user = request.user
    context = {}

    # context['usuGrupo'] = request.user.groups.all() # Precisa ser reavaliado
    print(request.user.groups.all())

    if user.justificar:
        context['tpJust'] = TipoJustificativa.objects.filter(sitJust=True) 
    if request.method == 'POST':
        if "btjustificar" in request.POST:
            if(user.justificar):
                processos.gravaJustificativa(request, user)
                return render(request, 'home/index.html', context) 
            else:
                return render(request, 'home/index.html', context)        
    else:
        registros = HistRegistro.objects.filter(userReg_id = user.id , dataReg = data.today())
        if registros:
            registro = HistRegistro.objects.get(userReg_id = user.id , dataReg = data.today())
            if ((registro.horEnt1 != None) and (registro.horSai2 == None)) or ((registro.horEnt1 != None) and (registro.horSai2 != None) and (registro.horEnt3 != None) and (registro.horSai4 == None)) :
                return render(request, 'home/index.html', context)
            else:
                horExtras =  HoraExtra.objects.filter(userExtra_id = user.id, dataExtra=data.today().date())
                if horExtras:
                    horExtra = HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date())
                    if ((horExtra.horEnt1 != None) and (horExtra.horSai2 == None)) or ((horExtra.horEnt1 != None) and (horExtra.horSai2 != None) and (horExtra.horEnt3 != None) and (horExtra.horSai4 == None)) :
                        return render(request, 'home/index.html', context) 
                    else:    
                        return redirect(RegistrarPonto)
                else:    
                    return redirect(RegistrarPonto) 
        else:
                horExtras =  HoraExtra.objects.filter(userExtra_id = user.id, dataExtra=data.today().date())
                if horExtras:
                    horExtra = HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date())
                    if ((horExtra.horEnt1 != None) and (horExtra.horSai2 == None)) or ((horExtra.horEnt1 != None) and (horExtra.horSai2 != None) and (horExtra.horEnt3 != None) and (horExtra.horSai4 == None)) :
                        return render(request, 'home/index.html', context) 
                    else:    
                        return redirect(RegistrarPonto)
                else:    
                    return redirect(RegistrarPonto)        
                

@login_required
def historico(request):
    context = {}
    user = request.user
    context['escalas'] = Escala.objects.filter(status=True)

    termoStatus = request.GET.get('status')
    termoJustificativa = request.GET.get('justificativa')
    termoData = request.GET.get('data')
    termoEscala = request.GET.get('escala')
    
    #Carrega registros Diarios
    registros = HistRegistro.objects.filter(Q(userReg__id = user.id)).order_by('-dataReg')
    if (termoStatus) or (termoJustificativa) or (termoData) or (termoEscala):
        filtros = Q()

        #Filtro por Status
        if(termoStatus == 'APR') or (termoStatus == 'PEN') or (termoStatus == 'REJ'):
            print(termoStatus)
            filtros &=  Q(sitAPR = termoStatus)
        
        #Filtro por Justificativa
        if(termoJustificativa != 'todas'):
            if (termoJustificativa == 'sim'):
                filtros &= ~Q(justificativas__isnull=True)           
            elif (termoJustificativa == 'nao'):
                filtros &= ~Q(justificativas__isnull=False)

        #Filtro por Data
        if(termoData):
            filtros &= Q(dataReg = termoData)

        #Filtro por Escala
        if termoEscala != 'todas':
            filtros &= Q(escala_id = termoEscala)

        registros = registros.filter(filtros).order_by('-dataReg')

    paginator = Paginator(registros, 10)
    page = request.GET.get('page')
    context['histReg'] = paginator.get_page(page)

    #Carrega Registros de Horas Extras
    HE = HoraExtra.objects.filter(userExtra_id = user.id).order_by('-dataExtra')
    if (termoStatus) or (termoJustificativa) or (termoData) or (termoEscala):
        filtrosHE = Q()
        #Filtro por Status
        if(termoStatus == 'APR') or (termoStatus == 'PEN') or (termoStatus == 'REJ'):
            filtrosHE &=  Q(sitAPR = termoStatus)
        
        #Filtro por Justificativa
        if(termoJustificativa != 'todas'):
            if (termoJustificativa == 'sim'):         
                filtrosHE &= ~Q(justificativas__isnull=True)           
            elif (termoJustificativa == 'nao'):
                filtrosHE &= ~Q(justificativas__isnull=False)

        #Filtro por Data
        if(termoData):
            filtrosHE &= Q(dataExtra = termoData)                                         
        
        #Carrega registros Diarios
        HE = HE.filter(filtrosHE).order_by('-dataExtra')

    paginator = Paginator(HE, 10)
    page = request.GET.get('page')
    context['regHE'] = paginator.get_page(page)

    if user.justificar:
        context['tpJust'] = TipoJustificativa.objects.filter(sitJust=True)
    if request.method == 'POST':
        if "btjustificar" in request.POST:
            if(user.justificar):
                processos.gravaJustificativa(request, user)
                return render(request, 'historico/index.html', context)
            else:
                return render(request, 'historico/index.html', context)
            
        elif "btAltReg" in request.POST:
                    inpId = request.POST.get('inpID')
                    historico = HistRegistro.objects.get(id = inpId)
                    ent1 = request.POST.get('ent1')
                    sai1 = request.POST.get('sai1')
                    ent2 = request.POST.get('ent2')
                    sai2 = request.POST.get('sai2')
                    if historico.horEnt1 != parse_time(ent1):
                        print('Primeiro')
                        historico.horEnt1 = hora.strptime(ent1, '%H:%M').time()
                        historico.altEnt1 = True

                    if historico.horSai2 != parse_time(sai1):
                        print('Segundo')
                        historico.horSai2 = hora.strptime(sai1, '%H:%M').time()
                        historico.altSai2 = True

                    if historico.horEnt3 != parse_time(ent2):
                        print('Terceiro')   
                        historico.horEnt3 = hora.strptime(ent2, '%H:%M').time()
                        historico.altEnt3 = True

                    if historico.horSai4 != parse_time(sai2):
                        print('Quarto')
                        historico.horSai4 = hora.strptime(sai2, '%H:%M').time()
                        historico.altSai4 = True
                    historico.userAlt = user
                    historico.dataAlt = data.today().date()    
                    historico.save()
                    messages.success(request, 'Registro Alterado com Sucesso!!')    
        elif "btAltRegHe" in request.POST:
                    inpId = request.POST.get('inpIDHe')
                    historico = HoraExtra.objects.get(id = inpId)
                    ent1 = request.POST.get('ent1He')
                    sai1 = request.POST.get('sai1He')
                    ent2 = request.POST.get('ent2He')
                    sai2 = request.POST.get('sai2He')

                    if historico.horEnt1 != parse_time(ent1):
                        print('Primeiro')
                        historico.horEnt1 = hora.strptime(ent1, '%H:%M').time()
                        historico.altEnt1 = True

                    if historico.horSai2 != parse_time(sai1):
                        print('Segundo')
                        historico.horSai2 = hora.strptime(sai1, '%H:%M').time()
                        historico.altSai2 = True

                    if historico.horEnt3 != parse_time(ent2):
                        print('Terceiro')   
                        historico.horEnt3 = hora.strptime(ent2, '%H:%M').time()
                        historico.altEnt3 = True

                    if historico.horSai4 != parse_time(sai2):
                        print('Quarto')
                        historico.horSai4 = hora.strptime(sai2, '%H:%M').time()
                        historico.altSai4 = True
                    historico.userAltHe = user
                    historico.dataAlt = data.today().date()    
                    historico.save()
                    messages.success(request, 'Registro Alterado com Sucesso!!')


    if request.method == 'GET':
        if "filtrar" in request.GET:
            print('Filtrar')
            filtrosReg = Q(userReg__id = user.id)
            filtrosHE = Q(userExtra__id = user.id)
            status = request.GET.get('status')
            justificativa = request.GET.get('justificativa')
            date = request.GET.get('data')
            escala = request.GET.get('escala')
            
            #Filtro por Status
            if(status == 'APR') or (status == 'PEN') or (status == 'REJ'):
                filtrosReg &=  Q(sitAPR = status)
                filtrosHE &=  Q(sitAPR = status)
            
            #Filtro por Justificativa
            if(justificativa != 'todas'):
                if (justificativa == 'sim'):
                    filtrosReg &= ~Q(justificativas__isnull=True)           
                    filtrosHE &= ~Q(justificativas__isnull=True)           
                elif (justificativa == 'nao'):
                    filtrosReg &= ~Q(justificativas__isnull=False)
                    filtrosHE &= ~Q(justificativas__isnull=False)

            #Filtro por Data
            if(date):
                filtrosReg &= Q(dataReg = date)
                filtrosHE &= Q(dataExtra = date)

            #Filtro por Escala
            if escala != 'todas':
                filtrosReg &= Q(escala_id = escala)                                            
            
            #Carrega registros Diarios
            registros = HistRegistro.objects.filter(filtrosReg).order_by('-dataReg')  
            paginator = Paginator(registros, 10)
            page = request.GET.get('page')
            context['histReg'] = paginator.get_page(page) 

            #Carrega Registros de Horas Extras
            HE = HoraExtra.objects.filter(filtrosHE).order_by('-dataExtra')
            paginator = Paginator(HE, 10)
            page = request.GET.get('page')
            context['regHE'] = paginator.get_page(page)
            if (not registros) and (not HE):
                messages.warning(request, 'Não possue registros Diarios e nem Horas Extras para o filtro utilizado!')

        #Gerar e Exportar PDF de Cartão ponto conforme a competência 
        print("exportar" in request.GET)
        if "exportar" in request.GET:
            comp = request.GET.get('periodoCP')
            if "/" in comp:
                mes, ano = comp.split('/')
                if (mes != '') and (ano != ''):
                    context = {}

                    # Pega a data atual
                    data_atual = data.strptime(('01/'+mes+'/'+ano), '%d/%m/%Y')

                    # Pega o primeiro dia do mês atual
                    primeiro_dia_mes = data_atual.replace(day=1)
                    # Pega o último dia do mês atual
                    _, ultimo_dia_mes = calendar.monthrange(data_atual.year, data_atual.month)
                    registros = {}

                    # Percorre do primeiro dia até o último dia do mês
                    for dia in range(primeiro_dia_mes.day, ultimo_dia_mes + 1):
                        datas = primeiro_dia_mes.replace(day=dia)
                        feriado = None
                        if Feriado.objects.filter(data = datas).exists():
                            feriado = Feriado.objects.get(data = datas).data
                        he = None    
                        if HoraExtra.objects.filter(userExtra_id = user.id, dataExtra=datas):
                                he = HoraExtra.objects.get(userExtra_id = user.id, dataExtra=datas)    
                        hist = HistRegistro.objects.filter(Q(userReg__id = user.id), dataReg = datas)
                        if hist:
                            dt = serialize('json', hist)
                            dtJson = json.loads(dt)
                            dtJson[0]['fields']['tpReg']= 'Comum'
                            if he is not None:
                                dtJson[0]['fields']['qtdHE'] = str(he.diff_formatted)
                            else:
                                dtJson[0]['fields']['qtdHE'] = '00:00'      
                            registros[datas] = dtJson
                        
                        else:
                            numDiaSemana = datas.weekday()
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
                            

                            if he is not None:
                                registros[datas] = [{'model': 'home.histregistro', 'pk': 0, 'fields': {'userReg': user.id, 'escala': '', 'dataReg': str(datas.date()), 'horEnt1': he.horEnt1, 'altEnt1': he.altEnt1, 'horSai2': he.horSai2, 'altSai2': he.altSai2, 'horEnt3': he.horEnt3, 'altEnt3': he.altEnt3, 'horSai4': he.horSai4, 'altSai4': he.altSai4, 'sitAPR': he.sitAPR, 'justificativas': he.justificativas, 'tpReg': 'Hora Extra', 'qtdHE': he.diff_formatted}}] 
                            
                            elif not diaSemana:
                                registros[datas] = [{'model': 'home.histregistro', 'pk': 0, 'fields': {'userReg': user.id, 'escala': None, 'dataReg': str(datas.date()), 'horEnt1': 'Folga', 'altEnt1': False, 'horSai2': 'Folga', 'altSai2': False, 'horEnt3': 'Folga', 'altEnt3': False, 'horSai4': 'Folga', 'altSai4': False, 'sitAPR': '', 'justificativas': 0, 'tpReg': '', 'qtdHE': '00:00'}}]   
                            
                            elif feriado == datas:
                                registros[datas] = [{'model': 'home.histregistro', 'pk': 0, 'fields': {'userReg': user.id, 'escala': '', 'dataReg': str(datas.date()), 'horEnt1': feriado.nome, 'altEnt1': False, 'horSai2': feriado.nome, 'altSai2': False, 'horEnt3': feriado.nome, 'altEnt3': False, 'horSai4': feriado.nome, 'altSai4': False, 'sitAPR': 'N/A', 'justificativas': 0, 'tpReg': 'N/A', 'qtdHE': '00:00'}}] 
                            
                            elif not datas < data.today():
                                registros[datas] = [{'model': 'home.histregistro', 'pk': 0, 'fields': {'userReg': user.id, 'escala': None, 'dataReg': str(datas.date()), 'horEnt1': 'Sem Registro', 'altEnt1': False, 'horSai2': 'Sem Registro', 'altSai2': False, 'horEnt3': 'Sem Registro', 'altEnt3': False, 'horSai4': 'Sem Registro', 'altSai4': False, 'sitAPR': 'N/A', 'justificativas': 0, 'tpReg': 'N/A', 'qtdHE': '00:00'}}]   

                            else:
                                registros[datas] = [{'model': 'home.histregistro', 'pk': 0, 'fields': {'userReg': user.id, 'escala': None, 'dataReg': str(datas.date()), 'horEnt1': 'Sem Registro', 'altEnt1': False, 'horSai2': 'Sem Registro', 'altSai2': False, 'horEnt3': 'Sem Registro', 'altEnt3': False, 'horSai4': 'Sem Registro', 'altSai4': False, 'sitAPR': 'N/A', 'justificativas': 0, 'tpReg': 'N/A', 'qtdHE': '00:00'}}]   
                        

                    context['registros'] = registros.items()
                    context['periodo'] = comp
                    context['user']= user 
                    pdf = processos.geraHtmlToPdf("cartaoPonto/index.html", context)
                    return JsonResponse({'mensage': 'Arquivo exportado com sucesso!', 'tipo':'text-bg-success', 'sit':'OK', 'pdf_base64': pdf })
                return JsonResponse({'mensage': 'Data informada Incorretamente!', 'tipo':'text-bg-danger', 'sit':'Erro' })
        else:
            registros = HistRegistro.objects.filter(userReg_id = user.id , dataReg = data.today())
            if registros:
                registro = HistRegistro.objects.get(userReg_id = user.id , dataReg = data.today())
                if ((registro.horEnt1 != None) and (registro.horSai2 == None)) or ((registro.horEnt1 != None) and (registro.horSai2 != None) and (registro.horEnt3 != None) and (registro.horSai4 == None)) :
                    return render(request, 'historico/index.html', context)
                else:
                    horExtras =  HoraExtra.objects.filter(userExtra_id = user.id, dataExtra=data.today().date())
                    if horExtras:
                        horExtra = HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date())
                        if ((horExtra.horEnt1 != None) and (horExtra.horSai2 == None)) or ((horExtra.horEnt1 != None) and (horExtra.horSai2 != None) and (horExtra.horEnt3 != None) and (horExtra.horSai4 == None)) :
                            return render(request, 'historico/index.html', context)
                        else:    
                            return redirect(RegistrarPonto)                        
                    else:    
                        return redirect(RegistrarPonto) 
            else :
                horExtras =  HoraExtra.objects.filter(userExtra_id = user.id, dataExtra=data.today().date())
                if horExtras:
                    horExtra = HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date())
                    if ((horExtra.horEnt1 != None) and (horExtra.horSai2 == None)) or ((horExtra.horEnt1 != None) and (horExtra.horSai2 != None) and (horExtra.horEnt3 != None) and (horExtra.horSai4 == None)) :
                        return render(request, 'historico/index.html', context)
                    else:    
                            return redirect(RegistrarPonto) 
                else:    
                    return redirect(RegistrarPonto) 

    return render(request, 'historico/index.html', context)

@login_required
def aprovaPonto(request):
    context = {}
    user = request.user

    if (user.groups.filter(name='Desenvolvedor').exists()) or (user.groups.filter(name='Coordenador').exists()):


        termoNome = request.GET.get('nome')
        termoMatricula = request.GET.get('matricula')
        termoStatus = request.GET.get('status')
        termoJustificativa = request.GET.get('justificativa')
        termoData = request.GET.get('data')
        termoEscala = request.GET.get('escala')

        registros = HistRegistro.objects.filter(Q(userReg__superior__id = user.id), Q(sitAPR='PEN')).order_by('-dataReg')
        if (termoNome) or (termoMatricula) or (termoStatus) or (termoJustificativa) or (termoData) or (termoEscala):
            filtros = Q()
            if termoNome:    
                filtros &= Q(userReg__first_name__icontains=termoNome) | Q(userReg__last_name__icontains=termoNome)
            
            #Filtro por Matricula
            if(termoMatricula):
                filtros &= Q(userReg__matricula = termoMatricula)
            
            #Filtro por Status
            if(termoStatus == 'APR') or (termoStatus == 'PEN') or (termoStatus == 'REJ'):
                print(termoStatus)
                filtros &=  Q(sitAPR = termoStatus)
            
            #Filtro por Justificativa
            if(termoJustificativa != 'todas'):
                if (justificativa == 'sim'):
                    filtros &= ~Q(justificativas__isnull=True)           
                elif (justificativa == 'nao'):
                    filtros &= ~Q(justificativas__isnull=False)

            #Filtro por Data
            if(termoData):
                filtros &= Q(dataReg = termoData)

            #Filtro por Escala
            if termoEscala != 'todas':
                filtros &= Q(escala_id = termoEscala)

            registros = registros.filter(filtros).order_by('-dataReg')

        context['escalas'] = Escala.objects.filter(status=True)
        paginator = Paginator(registros, 10)
        page = request.GET.get('page')
        context['histReg'] = paginator.get_page(page)
        if user.justificar:
            context['tpJust'] = TipoJustificativa.objects.filter(sitJust=True)

        
        filtros = Q(userReg__superior__id = user.id)
        nome = request.GET.get('nome')
        matricula = request.GET.get('matricula')
        status = request.GET.get('status')
        justificativa = request.GET.get('justificativa')
        date = request.GET.get('data')
        escala = request.GET.get('escala') 
        if request.method == 'POST':
            if "btjustificar" in request.POST:
                if(user.justificar):
                    processos.gravaJustificativa(request, user)
                    return render(request, 'aprovaPonto/index.html',context)
                else:
                    return render(request, 'aprovaPonto/index.html',context)          
                
            elif "btAltReg" in request.POST:
                    inpId = request.POST.get('inpID')
                    historico = HistRegistro.objects.get(id = inpId)
                    ent1 = request.POST.get('ent1')
                    sai1 = request.POST.get('sai1')
                    ent2 = request.POST.get('ent2')
                    sai2 = request.POST.get('sai2')
                    obsSup = request.POST.get('obsSup')

                    if historico.horEnt1 != parse_time(ent1):
                        print('Primeiro')
                        historico.horEnt1 = hora.strptime(ent1, '%H:%M').time()
                        historico.altEnt1 = True

                    if historico.horSai2 != parse_time(sai1):
                        print('Segundo')
                        historico.horSai2 = hora.strptime(sai1, '%H:%M').time()
                        historico.altSai2 = True

                    if historico.horEnt3 != parse_time(ent2):
                        print('Terceiro')   
                        historico.horEnt3 = hora.strptime(ent2, '%H:%M').time()
                        historico.altEnt3 = True

                    if historico.horSai4 != parse_time(sai2):
                        print('Quarto')
                        historico.horSai4 = hora.strptime(sai2, '%H:%M').time()
                        historico.altSai4 = True
                    historico.userAlt = user
                    historico.dataAlt = data.today().date()    
                    historico.obsSup = obsSup  
                    historico.save()
                    messages.success(request, 'Registro Alterado com Sucesso!!')
            else:
                print("Sem justificativa")
        
            return render(request, 'aprovaPonto/index.html',context)
        elif request.method == 'GET':
            print("GET")
            print(justificativa)
            if "filtrar" in request.GET:
                print('Filtrar')
                
                #Filtro por Nome
                if(nome):
                    filtros &= Q(userReg__first_name__icontains=nome) | Q(userReg__last_name__icontains=nome)
                
                #Filtro por Matricula
                if(matricula):
                    filtros &= Q(userReg__matricula = matricula)
                
                #Filtro por Status
                if(status == 'APR') or (status == 'PEN') or (status == 'REJ'):
                    filtros &=  Q(sitAPR = status)
                
                #Filtro por Justificativa
                if(justificativa != 'todas'):
                    if (justificativa == 'sim'):
                        filtros &= ~Q(justificativas__isnull=True)           
                    elif (justificativa == 'nao'):
                        filtros &= ~Q(justificativas__isnull=False)

                #Filtro por Data
                if(date):
                    filtros &= Q(dataReg = date)

                #Filtro por Escala
                if escala != 'todas':
                    filtros &= Q(escala_id = escala)                       
                
                registros = HistRegistro.objects.filter(filtros).order_by('-dataReg')  
                if not registros:
                    messages.warning(request, 'Não possue registros para o filtro utilizado!')

                paginator = Paginator(registros, 10)
                page = request.GET.get('page')
                context['histReg'] = paginator.get_page(page) 
            else:
                registros = HistRegistro.objects.filter(userReg_id = user.id , dataReg = data.today())
                if registros:
                    registro = HistRegistro.objects.get(userReg_id = user.id , dataReg = data.today())
                    if ((registro.horEnt1 != None) and (registro.horSai2 == None)) or ((registro.horEnt1 != None) and (registro.horSai2 != None) and (registro.horEnt3 != None) and (registro.horSai4 == None)) :
                        return render(request, 'aprovaPonto/index.html',context)
                    else:
                        horExtras =  HoraExtra.objects.filter(userExtra_id = user.id, dataExtra=data.today().date())
                        if horExtras:
                            horExtra = HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date())
                            if ((horExtra.horEnt1 != None) and (horExtra.horSai2 == None)) or ((horExtra.horEnt1 != None) and (horExtra.horSai2 != None) and (horExtra.horEnt3 != None) and (horExtra.horSai4 == None)) :
                                return render(request, 'aprovaPonto/index.html',context) 
                            else:    
                                return redirect(RegistrarPonto) 
                        else:    
                            return redirect(RegistrarPonto) 
                else :
                    horExtras =  HoraExtra.objects.filter(userExtra_id = user.id, dataExtra=data.today().date())
                    if horExtras:
                        horExtra = HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date())
                        if ((horExtra.horEnt1 != None) and (horExtra.horSai2 == None)) or ((horExtra.horEnt1 != None) and (horExtra.horSai2 != None) and (horExtra.horEnt3 != None) and (horExtra.horSai4 == None)) :
                            return render(request, 'aprovaPonto/index.html',context) 
                        else:    
                                return redirect(RegistrarPonto) 
                    else:    
                        return redirect(RegistrarPonto) 

        return render(request, 'aprovaPonto/index.html',context)
    else:
       return redirect(inicio) 



@login_required
def aprovar(request, id): 
    context = {}
    user = request.user
    if (user.groups.filter(name='Desenvolvedor').exists()) or (user.groups.filter(name='Coordenador').exists()):
        context['histReg'] = HistRegistro.objects.filter(Q(userReg__superior__id = user.id), Q(sitAPR='PEN'))
        historico = HistRegistro.objects.get(id = id)
        historico.sitAPR = 'APR'
        historico.userAlt = user
        historico.dataAlt = data.today().date()
        historico.save()
        processos.enviaEmail(historico.userReg.email, 'Aprovado', 'Registro de Ponto Aprovado - Ponto Seguro', historico.dataReg, historico.obsSup, historico.horEnt1, historico.horSai2, historico.horEnt3, historico.horSai4)
        # messages.success(request, 'Registro Aprovado com Sucesso!')
        return render(request, 'parciais/tabela_aprovacao.html', context)
    else:
        return redirect(inicio)




@login_required
def desaprovar(request, id): 
    context = {}
    user = request.user
    if (user.groups.filter(name='Desenvolvedor').exists()) or (user.groups.filter(name='Coordenador').exists()):
        historico = HistRegistro.objects.get(id = id)
        historico.sitAPR = 'REJ'
        historico.userAlt = user
        historico.dataAlt = data.today().date()
        historico.save()
        context['histReg'] = HistRegistro.objects.filter(Q(userReg__superior__id = user.id), Q(sitAPR='PEN')) 
        processos.enviaEmail(historico.userReg.email, 'Reprovado', 'Registro de Ponto Rejeitado - Ponto Seguro', historico.dataReg, historico.obsSup, historico.horEnt1, historico.horSai2, historico.horEnt3, historico.horSai4)
        # messages.error(request, 'Registro Rejeitado com Sucesso!')
        return render(request, 'parciais/tabela_aprovacao.html', context)
    else:
            return redirect(inicio)



@login_required
def aprovaPontoHE(request):
    context = {}
    user = request.user
    if (user.groups.filter(name='Desenvolvedor').exists()) or (user.groups.filter(name='Coordenador').exists()):

        registros = HoraExtra.objects.filter(Q(userExtra__superior__id = user.id), Q(sitAPR='PEN')).order_by('-dataExtra')
        context['escalas'] = Escala.objects.filter(status=True)
        paginator = Paginator(registros, 10)
        page = request.GET.get('page')
        context['histReg'] = paginator.get_page(page)
        if user.justificar:
            context['tpJust'] = TipoJustificativa.objects.filter(sitJust=True)
        
        nome = request.GET.get('nome')
        matricula = request.GET.get('matricula')
        status = request.GET.get('status')
        justificativa = request.GET.get('justificativa')
        date = request.GET.get('data')
        escala = request.GET.get('escala') 
        if request.method == 'POST':
            print("POST")
            print(justificativa)
            if "btjustificar" in request.POST:
                if(user.justificar):
                    processos.gravaJustificativa(request, user)
                    return render(request, 'aprovaPontoHE/index.html',context)  
                else:
                    return render(request, 'aprovaPontoHE/index.html',context)          

            elif "btAltReg" in request.POST:
                    inpId = request.POST.get('inpID')
                    historico = HoraExtra.objects.get(id = inpId)
                    ent1 = request.POST.get('ent1')
                    sai1 = request.POST.get('sai1')
                    ent2 = request.POST.get('ent2')
                    sai2 = request.POST.get('sai2')
                    obsSup = request.POST.get('obsSup')

                    if historico.horEnt1 != parse_time(ent1):
                        print('Primeiro')
                        historico.horEnt1 = hora.strptime(ent1, '%H:%M').time()
                        historico.altEnt1 = True

                    if historico.horSai2 != parse_time(sai1):
                        print('Segundo')
                        historico.horSai2 = hora.strptime(sai1, '%H:%M').time()
                        historico.altSai2 = True

                    if historico.horEnt3 != parse_time(ent2):
                        print('Terceiro')   
                        historico.horEnt3 = hora.strptime(ent2, '%H:%M').time()
                        historico.altEnt3 = True

                    if historico.horSai4 != parse_time(sai2):
                        print('Quarto')
                        historico.horSai4 = hora.strptime(sai2, '%H:%M').time()
                        historico.altSai4 = True
                    historico.userAltHe = user
                    historico.dataAlt = data.today().date()    
                    historico.obsSup = obsSup    
                    historico.save()
                    messages.success(request, 'Registro Alterado com Sucesso!!')
            else:
                print("Sem justificativa")
        
            return render(request, 'aprovaPontoHE/index.html',context)
        elif request.method == 'GET':
            print("GET")
            if "filtrar" in request.GET:
                print('Filtrar')

                filtros = Q(userExtra__superior__id = user.id)

                #Filtro por Nome
                if(nome):
                    filtros &= Q(userExtra__first_name__icontains=nome) | Q(userExtra__last_name__icontains=nome)
                
                #Filtro por Matricula
                if(matricula):
                    filtros &= Q(userExtra__matricula = matricula)
                
                #Filtro por Status
                if(status == 'APR') or (status == 'PEN') or (status == 'REJ'):
                    filtros &=  Q(sitAPR = status)
                
                #Filtro por Justificativa
                if(justificativa != 'todas'):
                    if (justificativa == 'sim'):
                        filtros &= ~Q(justificativas__isnull=True)           
                    elif (justificativa == 'nao'):
                        filtros &= ~Q(justificativas__isnull=False)

                #Filtro por Data
                if(date):
                    filtros &= Q(dataExtra = date)

                #Filtro por Escala
                if escala != 'todas':
                    filtros &= Q(escala_id = escala)                       
                registros = HoraExtra.objects.filter(filtros).order_by('-dataExtra')  
                if not registros:
                    messages.warning(request, 'Não possue registros para o filtro utilizado!')

                paginator = Paginator(registros, 10)
                page = request.GET.get('page')
                context['histReg'] = paginator.get_page(page) 
                return render(request, 'aprovaPontoHE/index.html',context) 
            else: 
                registros = HistRegistro.objects.filter(userReg_id = user.id , dataReg = data.today())
                if registros:
                    registro = HistRegistro.objects.get(userReg_id = user.id , dataReg = data.today())
                    if ((registro.horEnt1 != None) and (registro.horSai2 == None)) or ((registro.horEnt1 != None) and (registro.horSai2 != None) and (registro.horEnt3 != None) and (registro.horSai4 == None)) :
                        return render(request, 'aprovaPontoHE/index.html',context)
                    else:
                        horExtras =  HoraExtra.objects.filter(userExtra_id = user.id, dataExtra=data.today().date())
                        if horExtras:
                            horExtra = HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date())
                            if ((horExtra.horEnt1 != None) and (horExtra.horSai2 == None)) or ((horExtra.horEnt1 != None) and (horExtra.horSai2 != None) and (horExtra.horEnt3 != None) and (horExtra.horSai4 == None)) :
                                return render(request, 'aprovaPontoHE/index.html',context) 
                            else:    
                                return redirect(RegistrarPonto) 
                        else:    
                            return redirect(RegistrarPonto) 
                else :
                    horExtras =  HoraExtra.objects.filter(userExtra_id = user.id, dataExtra=data.today().date())
                    if horExtras:
                        horExtra = HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date())
                        if ((horExtra.horEnt1 != None) and (horExtra.horSai2 == None)) or ((horExtra.horEnt1 != None) and (horExtra.horSai2 != None) and (horExtra.horEnt3 != None) and (horExtra.horSai4 == None)) :
                            return render(request, 'aprovaPontoHE/index.html',context) 
                        else:    
                                return redirect(RegistrarPonto) 
                    else:    
                        return redirect(RegistrarPonto) 
    else:
        return redirect(inicio)                 




@login_required
def aprovarHE(request, id): 
    context = {}
    user = request.user
    if (user.groups.filter(name='Desenvolvedor').exists()) or (user.groups.filter(name='Coordenador').exists()):
        historico = HoraExtra.objects.get(id = id)
        historico.sitAPR = 'APR'
        historico.userAltHe = user
        historico.dataAlt = data.today().date()
        historico.save()
        processos.enviaEmail(historico.userExtra.email, 'Aprovado', 'Registro de Ponto Extra Aprovado - Ponto Seguro', historico.dataExtra, historico.obsSup, historico.horEnt1, historico.horSai2, historico.horEnt3, historico.horSai4)

        context['histReg'] = HoraExtra.objects.filter(Q(userExtra__superior__id = user.id), Q(sitAPR='PEN'))
        return render(request, 'parciais/tabela_aprovacao_HE.html', context)
    else:
        return redirect(inicio)



@login_required
def desaprovarHE(request, id): 
    context = {}
    user = request.user
    if (user.groups.filter(name='Desenvolvedor').exists()) or (user.groups.filter(name='Coordenador').exists()):
        historico = HoraExtra.objects.get(id = id)
        historico.sitAPR = 'REJ'
        historico.userAltHe = user
        historico.dataAlt = data.today().date()
        historico.save()
        processos.enviaEmail(historico.userExtra.email, 'Reprovado', 'Registro de Ponto Extra Rejeitado - Ponto Seguro', historico.dataExtra, historico.obsSup, historico.horEnt1, historico.horSai2, historico.horEnt3, historico.horSai4)

        context['histReg'] = HoraExtra.objects.filter(Q(userExtra__superior__id = user.id), Q(sitAPR='PEN')) 
        return render(request, 'parciais/tabela_aprovacao_HE.html', context)
    else:
        return redirect(inicio)




@login_required
def escala(request):
    user = request.user
    if (user.groups.filter(name='Desenvolvedor').exists()) or (user.groups.filter(name='Coordenador').exists()):

        context = {}
        escalas = Escala.objects.all() 
        paginator = Paginator(escalas, 10)
        page = request.GET.get('page')
        context['escalas'] = paginator.get_page(page)
        context['usuarios'] = Users.objects.all()

        if request.method == 'POST':
            print('Entrou no POST')
            if "btjustificar" in request.POST:
                if(user.justificar):
                    processos.gravaJustificativa(request, user)
                    render(request, 'cadastroEscala/index.html', context)
                else:
                    render(request, 'cadastroEscala/index.html', context)     
                    
        elif request.method == 'GET':  
                print('Entrou Get')       
                registros = HistRegistro.objects.filter(userReg_id = user.id , dataReg = data.today())
                if registros:
                    registro = HistRegistro.objects.get(userReg_id = user.id , dataReg = data.today())
                    if ((registro.horEnt1 != None) and (registro.horSai2 == None)) or ((registro.horEnt1 != None) and (registro.horSai2 != None) and (registro.horEnt3 != None) and (registro.horSai4 == None)) :
                        render(request, 'cadastroEscala/index.html', context)
                    else:
                        horExtras =  HoraExtra.objects.filter(userExtra_id = user.id, dataExtra=data.today().date())
                        if horExtras:
                            horExtra = HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date())
                            if ((horExtra.horEnt1 != None) and (horExtra.horSai2 == None)) or ((horExtra.horEnt1 != None) and (horExtra.horSai2 != None) and (horExtra.horEnt3 != None) and (horExtra.horSai4 == None)) :
                                render(request, 'cadastroEscala/index.html', context)
                            else:    
                                return redirect(RegistrarPonto)      
                        else:    
                            return redirect(RegistrarPonto) 
                        
                else :
                    horExtras =  HoraExtra.objects.filter(userExtra_id = user.id, dataExtra=data.today().date())
                    if horExtras:
                        horExtra = HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date())
                        if ((horExtra.horEnt1 != None) and (horExtra.horSai2 == None)) or ((horExtra.horEnt1 != None) and (horExtra.horSai2 != None) and (horExtra.horEnt3 != None) and (horExtra.horSai4 == None)) :
                            render(request, 'cadastroEscala/index.html', context) 
                        else:    
                                return redirect(RegistrarPonto)     
                    else:    
                        return redirect(RegistrarPonto)                   
        return render(request, 'cadastroEscala/index.html', context)
    else:
        return redirect(inicio)





@login_required
def cadastroEscala(request):
    print('Cadastro de Escala')

    user = request.user
    if (user.groups.filter(name='Desenvolvedor').exists()) or (user.groups.filter(name='Coordenador').exists()):

        nmEscala = request.POST.get('nmEscala').strip()

        ent1 = request.POST.get('ent1')
        ent1 = hora.strptime(ent1, '%H:%M').time() if ent1 else None
        sai1 = request.POST.get('sai1')
        sai1 = hora.strptime(sai1, '%H:%M').time() if sai1 else None
        ent2 = request.POST.get('ent2')
        ent2 = hora.strptime(ent2, '%H:%M').time() if ent2 else None
        sai2 = request.POST.get('sai2')
        sai2 = hora.strptime(sai2, '%H:%M').time() if sai2 else None

        if(nmEscala != ''):
            if (ent1 != None) and (sai1 != None):
                seg = request.POST.get('seg', False) == 'on'
                terc = request.POST.get('terc', False) == 'on'
                quart = request.POST.get('quart', False) == 'on'
                quint = request.POST.get('quint', False) == 'on'
                sext = request.POST.get('sext', False) == 'on'
                sab = request.POST.get('sab', False) == 'on'
                domin = request.POST.get('domin', False) == 'on'
                if (seg == True) or (terc == True) or (quart == True) or (quint == True) or (sext == True) or (sab == True) or (domin == True):
                    newEscala = Escala.objects.create(nmEscala = nmEscala, 
                                        horEnt1 = ent1, 
                                        horSai2 = sai1,
                                        horEnt3 = ent2, 
                                        horSai4 = sai2, 
                                        segunda = seg, 
                                        terca= terc, 
                                        quarta = quart, 
                                        quinta = quint, 
                                        sexta = sext, 
                                        sabado = sab, 
                                        domingo = domin, 
                                        status = True) 
                    
                    return JsonResponse({'mensage':'Escala Gravada com Sucesso!', 'tipo':'text-bg-success', 'sit':'OK', 'escala':
                                         {'id': str(newEscala.id), 'nmEscala': newEscala.nmEscala, 
                                          
                                         'horEnt1': newEscala.horEnt1.strftime('%H:%M')  if newEscala.horEnt1 else '', 
                                         'horSai2': newEscala.horSai2.strftime('%H:%M')  if newEscala.horSai2 else '', 
                                         'horEnt3': newEscala.horEnt3.strftime('%H:%M')  if newEscala.horEnt3 else '', 
                                         'horSai4': newEscala.horSai4.strftime('%H:%M') if newEscala.horSai4 else '', 

                                         'segunda': 'checked' if newEscala.segunda else '', 
                                         'terca': 'checked' if  newEscala.terca else '', 'quarta':'checked' if  newEscala.quarta else '', 
                                         'quinta': 'checked' if newEscala.quinta else '', 'sexta': 'checked' if newEscala.sexta else '', 
                                         'sabado': 'checked' if newEscala.sabado else '', 'domingo': 'checked' if newEscala.domingo else '',
                                         'status': 'checked' if newEscala.status else '', 'statusTab': 'Ativo' if newEscala.status else 'Inativo'}}) 
                else:
                    return JsonResponse({'mensage':'Selecione um dia da Semana!', 'tipo':'text-bg-danger', 'sit':'ERRO'})  
            else:
                return JsonResponse({'mensage':'Informe ao menos a primeira Entrada e a Primeira Saída!!', 'tipo':'text-bg-danger', 'sit':'ERRO'}) 
        else:
            return JsonResponse({'mensage':'Informe a Descrição da Escala!', 'tipo':'text-bg-danger', 'sit':'ERRO'})  
    return JsonResponse({'mensage':'Você não Possui Acesso a Esta Funcinalidade!!', 'tipo':'text-bg-danger', 'sit':'ERRO'})




@login_required
def alteraEscala(request, id):
    print('Alteração de Escala')
    user = request.user
    if (user.groups.filter(name='Desenvolvedor').exists()) or (user.groups.filter(name='Coordenador').exists()):
        nmEscala = request.POST.get('nmEscala'+ str(id))
        ent1 = request.POST.get('ent1-'+ str(id))
        ent1 = hora.strptime(ent1, '%H:%M').time() if ent1 else None
        sai1 = request.POST.get('sai2-'+ str(id))
        sai1 = hora.strptime(sai1, '%H:%M').time() if sai1 else None
        ent2 = request.POST.get('ent3-'+ str(id))
        ent2 = hora.strptime(ent2, '%H:%M').time() if ent2 else None
        sai2 = request.POST.get('sai4-'+ str(id))
        sai2 = hora.strptime(sai2, '%H:%M').time() if sai2 else None
        if(nmEscala != ''):
            if (ent1 != None) and (sai1 != None):
                seg = request.POST.get('seg'+ str(id), False) == 'on'
                terc = request.POST.get('terc'+ str(id), False) == 'on'
                quart = request.POST.get('quart'+ str(id), False) == 'on'
                quint = request.POST.get('quint'+ str(id), False) == 'on'
                sext = request.POST.get('sext'+ str(id), False) == 'on'
                sab = request.POST.get('sab'+ str(id), False) == 'on'
                domin = request.POST.get('domin'+ str(id), False) == 'on'
                status = request.POST.get('sitEscala'+ str(id), False) == 'on'
                if (seg == True) or (terc == True) or (quart == True) or (quint == True) or (sext == True) or (sab == True) or (domin == True):
                    escala = Escala.objects.get(id=id)
                    escala.nmEscala = nmEscala
                    escala.horEnt1 = ent1
                    escala.horSai2 = sai1
                    escala.horEnt3 = ent2
                    escala.horSai4 = sai2
                    escala.segunda = seg
                    escala.terca = terc
                    escala.quarta = quart
                    escala.quinta = quint
                    escala.sexta = sext
                    escala.sabado = sab
                    escala.domingo = domin
                    escala.status = status
                    escala.save()

                    if escala.status == True:
                        situacao = 'Ativo'
                    else:
                        situacao = 'Inativo'

                    return JsonResponse({'mensage':'Escala Gravada com Sucesso!', 'tipo':'text-bg-success', 'sit': 'OK', 'escala': str(escala.nmEscala), 'status': situacao}) 
                else:
                    return JsonResponse({'mensage':'Selecione um dia da Semana!', 'tipo':'text-bg-danger', 'sit': 'ERRO'})  
            else:
                return JsonResponse({'mensage':'Informe ao menos a primeira Entrada e a Primeira Saída!!', 'tipo':'text-bg-danger', 'sit': 'ERRO'})  
        else:
            return JsonResponse({'mensage':'Informe a Descrição da Escala!', 'tipo':'text-bg-danger', 'sit': 'ERRO'})  
    else:
        return JsonResponse({'mensage':'Você não Possui Acesso a Esta Funcinalidade!!', 'tipo':'text-bg-danger', 'sit':'ERRO'})  
    


def usuarios(request):
    print('Informações dos Usuarios')
    user = request.user
    if (user.groups.filter(name='Desenvolvedor').exists()) or (user.groups.filter(name='Coordenador').exists()):
        context = {}
        context['usuarios'] = Users.objects.filter(superior_id = user.id)
        context['escalas'] = Escala.objects.all()
        context['cargos'] = Cargo.objects.all()
        return render(request, 'usuario/index.html', context)    
    else:
        return redirect(inicio)    



def altUsuario(request, id):
    print('Altera Informações dos Usuarios')
    user = request.user
    if (user.groups.filter(name='Desenvolvedor').exists()) or (user.groups.filter(name='Coordenador').exists()):
        primeiroNome = request.POST.get('primeiroNome'+ str(id))
        sobrenome = request.POST.get('sobrenome'+ str(id))
        escalas = request.POST.get('escalas'+ str(id))
        email = request.POST.get('email'+ str(id))
        cargos = request.POST.get('cargos'+ str(id))
        if (primeiroNome != '') and (sobrenome != '') and (escalas != '') and (email != '') and (cargos != ''):
            if '@' in email and '.' in email:
                userAlt = Users.objects.get(id = id)
                escala = Escala.objects.get(id = escalas)
                cargo = Cargo.objects.get(id = cargos)

                userAlt.first_name = primeiroNome
                userAlt.last_name = sobrenome
                userAlt.escala = escala
                userAlt.email = email
                userAlt.cargo = cargo
                userAlt.save()
                
                return JsonResponse({'mensage':'Usuario Alterado Com Sucesso!!', 'tipo':'text-bg-success', 'nomeComp': str(userAlt.first_name + ' ' + userAlt.last_name), 'escala': str(userAlt.escala.nmEscala), 'email': str(userAlt.email), 'cargo': str(userAlt.cargo.nmCargo), 'sit':'OK'}) 
            else:
                return JsonResponse({'mensage':'E-mail Digitado Incorreto!!', 'tipo':'text-bg-danger', 'sit':'ERRO'})
        else:
            return JsonResponse({'mensage':'Todos os Campos Devem Estar Preenchidos!!', 'tipo':'text-bg-danger', 'sit':'ERRO'})
    
    else:
        return JsonResponse({'mensage':'Você não Possui Acesso a Esta Funcinalidade!!', 'tipo':'text-bg-danger', 'sit':'ERRO'})
