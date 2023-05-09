from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import HistRegistro, HoraExtra, TipoJustificativa, Justificativa
import calendar
from datetime import datetime as hora, datetime as data, timedelta
from django.utils.dateparse import parse_time
from django.contrib import messages, auth
from django.http import HttpResponse
from accounts import views
from django.db.models import Q

#Paginação Django
from django.core.paginator import Paginator

#Envio de E-mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

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
                    HistRegistro.objects.create(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date(), horEnt1=ha.strftime('%H:%M')) 


                    #Validação para adicionar dados ao banco de horas
                    altHist = HistRegistro.objects.get(userReg_id = user.id, escala_id = user.escala.id, dataReg = data.today().date())
                    horPercorridas =  hora.combine(hora.today(), user.escala.horEnt1) - hora.combine(hora.today(), ha) 
                    if (hora.combine(hora.today(), ha) < hora.combine(hora.today(), horaEnt1_subtrai)):
                        print('É menor que o horario da escala Então Saldo é positivo')
                        horPercorridas =  hora.combine(hora.today(), user.escala.horEnt1) - hora.combine(hora.today(), ha) 
                        print(horPercorridas.seconds// 60)
                        altHist.bancoHoraMin = horPercorridas.seconds// 60

                    elif (hora.combine(hora.today(), horaEnt1_soma) < hora.combine(hora.today(), ha)):
                        print('É maior que o horario da escala Então Saldo Negativo')
                        horPercorridas =  hora.combine(hora.today(), ha) - hora.combine(hora.today(), user.escala.horEnt1) 
                        print(-(horPercorridas.seconds// 60))

                        user.justificar = True
                        user.save()

                        altHist.bancoHoraMin = -(horPercorridas.seconds// 60)
                        
                    
                    
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

                        horPercorridas =  hora.combine(hora.today(), user.escala.horSai2) - hora.combine(hora.today(), ha)
                        print(horPercorridas) 
                        print(horPercorridas.seconds// 60)
                        print(altHist.bancoHoraMin)
                        
                        user.justificar = True
                        user.save()

                        if (altHist.bancoHoraMin < 0 ):
                            altHist.bancoHoraMin = altHist.bancoHoraMin +  (-(horPercorridas.seconds// 60))
                        else:
                            altHist.bancoHoraMin = (-(horPercorridas.seconds// 60)) + altHist.bancoHoraMin    

                    elif (hora.combine(hora.today(), horaSai2_soma) > hora.combine(hora.today(), ha)):
                        print('Escala é maior que o horario atual Então Saldo Positivo')

                        horPercorridas = hora.combine(hora.today(), ha) - hora.combine(hora.today(), user.escala.horSai2)

                        if (altHist.bancoHoraMin < 0 ):
                            altHist.bancoHoraMin =  altHist.bancoHoraMin + (horPercorridas.seconds// 60)
                        else:
                            altHist.bancoHoraMin = (horPercorridas.seconds// 60) + altHist.bancoHoraMin    
                    
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


                            elif (hora.combine(hora.today(), horaEnt3_soma) < hora.combine(hora.today(), ha)):
                                print('É maior que o horario padrão Então Saldo Negativo')

                                horPercorridas = hora.combine(hora.today(), ha) - hora.combine(hora.today(), user.escala.horEnt3)
                                
                                user.justificar = True
                                user.save()

                                if (altHist.bancoHoraMin > 0 ):
                                    altHist.bancoHoraMin = altHist.bancoHoraMin +  (-(horPercorridas.seconds// 60))
                                else:
                                    altHist.bancoHoraMin = (-(horPercorridas.seconds// 60)) + altHist.bancoHoraMin

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

                        horPercorridas =  hora.combine(hora.today(), user.escala.horSai4) - hora.combine(hora.today(), ha)
                        print(horPercorridas) 
                        print(horPercorridas.seconds// 60)
                        print(altHist.bancoHoraMin)

                        user.justificar = True
                        user.save()

                        if (altHist.bancoHoraMin < 0 ):
                            altHist.bancoHoraMin = altHist.bancoHoraMin +  (-(horPercorridas.seconds// 60))
                        else:
                            altHist.bancoHoraMin = (-(horPercorridas.seconds// 60)) + altHist.bancoHoraMin    

                    elif (hora.combine(hora.today(), horaSai4_soma) < hora.combine(hora.today(), ha)):
                        print('É maior que o horario padrão Então Saldo Negativo')

                        horPercorridas = hora.combine(hora.today(), ha) - hora.combine(hora.today(), user.escala.horSai4)

                        if (altHist.bancoHoraMin < 0 ):
                            altHist.bancoHoraMin =  altHist.bancoHoraMin + (horPercorridas.seconds// 60)
                        else:
                            altHist.bancoHoraMin = (horPercorridas.seconds// 60) + altHist.bancoHoraMin    
                    altHist.save()  
                    messages.success(request, f'Quarta Saida Registrada com Sucesso {str(altHist.horSai4)[:-6]}') 
                    auth.logout(request)
                    return redirect(views.login)

                else:
                    if not HoraExtra.objects.filter(userExtra_id = user.id, dataExtra=data.today().date()):
                        HoraExtra.objects.create(userExtra_id = user.id, dataExtra=data.today().date(), horEnt1=ha.strftime('%H:%M')) 
                        messages.success(request, f'Primeira Entrada Extra Registrada com Sucesso {str(HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date()).horEnt1)[:-6]}') 
                        return redirect(inicio)
                    else:
                        horExtra = HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date())     
                        if horExtra.horSai2 is None:
                            horExtra.horSai2 = ha.strftime('%H:%M')
                            messages.success(request, f'Segunda Saida Extra Registrada com Sucesso {str(horExtra.horSai2)[:-6]}') 
                            horExtra.save()
                            auth.logout(request)
                            return redirect(views.login)
                            # return render(request, 'registraPonto/index.html', context)
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
                            # return render(request, 'registraPonto/index.html', context)      
            
            #    messages.error(request, "Você está fora da sua escala de trabalho!")
            #    return render(request, 'registraPonto/index.html', context) 
        else:
            if not HoraExtra.objects.filter(userExtra_id = user.id, dataExtra=data.today().date()):
                        HoraExtra.objects.create(userExtra_id = user.id, dataExtra=data.today().date(), horEnt1=ha.strftime('%H:%M'))
                        messages.success(request, f'Primeira Entrada Extra Registrada com Sucesso {str(HoraExtra.objects.get(userExtra_id = user.id, dataExtra=data.today().date()).horEnt1)}')
                        # return render(request, 'registraPonto/index.html', context)
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
                    
                   
            
        # return render(request, 'registraPonto/index.html', context)     
    else:    
        return render(request, 'registraPonto/index.html', context)

@login_required
def inicio(request):
    user = request.user
    context = {}
    context['tpJust'] = TipoJustificativa.objects.filter(sitJust=True)
    print(TipoJustificativa.objects.filter(sitJust=True))
    if request.method == 'POST':
        if "btjustificar" in request.POST:
            print("Este method é De envio de justificativa")
            tipoJust = request.POST.get('tipoJust')
            txtJust = request.POST.get('txtJust').strip()
            print(tipoJust)
            print(txtJust)
            if(tipoJust is None):
                messages.error(request, 'Informe um tipo de Justificativa!')
                return redirect("inicio")
            elif(txtJust == ''):
                messages.error(request, 'Digite o Motivo do Atraso!')  
                
            else:
                histRegistro = HistRegistro.objects.get(userReg = user.id,  escala_id = user.escala.id, dataReg = data.today().date())
                Justificativa.objects.create(txtJust = txtJust, tipoJust_id = tipoJust, histRegistro_id = histRegistro.id, data = data.today(), hora = hora.now().time(), userReg_id = user.id)
                user.justificar = False
                user.save()
                messages.success(request, 'Justificativa Registrada com Sucesso')
            return redirect("inicio")

        else:
            print("Sem justificativa")

            return render(request, 'home/index.html', context)
    else:
        return render(request, 'home/index.html', context)
    
@login_required
def mostrahtml(request):
    # botao = request.POST.get('hx-request')
    # botao = request.body.get('hist')
    # botao = request.headers.get('')
    botao = request.POST.get('hist')
    print(botao)
    print("Request acima")
    if  botao == 'historico':  #'historico' in request.GET:
        return HttpResponse(f'''<embed class="tamanhos removeScrol" id="mostraHTML" src="{reverse('historico')}" type="">''')
    elif botao ==  "aprovaPonto":
        return HttpResponse(f'''<embed class="tamanhos removeScrol" id="mostraHTML" src="{reverse('aprovaPonto')}" type="">''')
    elif botao == "cadastroEscalas":
        return HttpResponse(f'''<embed class="tamanhos removeScrol" id="mostraHTML" src="{reverse('cadastroEscalas')}" type="">''')
    else:
        return HttpResponse(f'''<embed class="tamanhos removeScrol" id="mostraHTML" src="{reverse('aprovaPonto')}" type="">''')

@login_required
def historico(request):
    return render(request, 'historico/index.html')

@login_required
def aprovaPonto(request):
    context = {}
    user = request.user
    registros = HistRegistro.objects.filter(Q(userReg__superior__id = user.id), Q(sitAPR='PEN'))
    # context['tpJust'] = TipoJustificativa.objects.filter(sitJust=True)
    paginator = Paginator(registros, 10)
    page = request.GET.get('page')
    context['histReg'] = paginator.get_page(page)
    if request.method == 'POST':
        if "btjustificar" in request.POST:
            print("Este method é De envio de justificativa")
            tipoJust = request.POST.get('tipoJust')
            txtJust = request.POST.get('txtJust').strip()
            print(tipoJust)
            print(txtJust)
            if(tipoJust is None):
                messages.error(request, 'Informe um tipo de Justificativa!')
                return redirect("aprovaPonto")
            elif(txtJust == ''):
                messages.error(request, 'Digite o Motivo do Atraso!')  
                
            else:
                histRegistro = HistRegistro.objects.get(userReg = user.id,  escala_id = user.escala.id, dataReg = data.today().date())
                Justificativa.objects.create(txtJust = txtJust, tipoJust_id = tipoJust, histRegistro_id = histRegistro.id, data = data.today(), hora = hora.now().time(), userReg_id = user.id)
                user.justificar = False
                user.save()
                messages.success(request, 'Justificativa Registrada com Sucesso')
            return redirect("aprovaPonto")

        else:
            print("Sem justificativa")
    
        return render(request, 'aprovaPonto/index.html',context)
    else:
        return render(request, 'aprovaPonto/index.html',context)

@login_required
def justificativas(request, id):
    historico = HistRegistro.objects.get(id = id)
    justificativas = Justificativa.objects.filter(histRegistro_id = historico.id)
    mostraJust = ''
    for just in justificativas:
        mostraJust += f'Tipo de Justificativa: {just.tipoJust} <br>Resposta: {just.txtJust} <br>Data: {just.data} <br><br>'

    return HttpResponse(f'''  <div class="modal fade show" id="modal" tabindex="-1" style="display: block; background-color: #00000057;" aria-modal="true" role="dialog">
    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
      <div class="modal-content">
        <div class="modal-header">
          <h1 class="modal-title fs-5" >Justificativa</h1>
          <button type="button" class="btn-close" onclick="fecharModal()" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p>{mostraJust}</p>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" onclick="fecharModal()">Fechar</button>
        </div>
      </div>
    </div>
  </div>''')

@login_required
def ajuste(request, id):
    historico = HistRegistro.objects.get(id = id)

    return render(request, 'parciais/modal_alt_Reg.html', {'historico': historico}) 

@login_required    
def altRegistro(request, id):
    print('teste')
    historico = HistRegistro.objects.get(id = id)
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
    historico.save()
    messages.success(request, 'Registro Alterado com Sucesso!!')

    return redirect('aprovaPonto')

@login_required
def aprovar(request, id): 
    context = {}
    user = request.user
    context['histReg'] = HistRegistro.objects.filter(Q(userReg__superior__id = user.id), Q(sitAPR='PEN'))
    historico = HistRegistro.objects.get(id = id)
    historico.sitAPR = 'APR'
    historico.save()
    messages.success(request, 'Registro Aprovado com Sucesso!')
    return render(request, 'parciais/tabela_aprovacao.html', context)

@login_required
def desaprovar(request, id): 
    context = {}
    user = request.user
    context['histReg'] = HistRegistro.objects.filter(Q(userReg__superior__id = user.id), Q(sitAPR='PEN')) 
    historico = HistRegistro.objects.get(id = id)
    historico.sitAPR = 'REJ'
    historico.save()
    enviaEmail('vitorkuhnen14@gmail.com', 'Vítor')
    messages.error(request, 'Registro Rejeitado com Sucesso!')
    return render(request, 'parciais/tabela_aprovacao.html', context)




def enviaEmail(email, user):
    # html_content = render_to_string('email/token.html', {'token': token})
    # text_content = strip_tags(html_content)
    email = EmailMultiAlternatives('PontoSeguro - Token de Identificação', '12', settings.EMAIL_HOST_USER, [email])
    # email.attach_alternative(html_content, 'text/html')
    email.send()
    return "enviado"