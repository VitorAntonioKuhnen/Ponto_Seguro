from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import HistRegistro
from accounts.models import Users
import calendar
import datetime as data
from datetime import datetime as hora, timedelta
from django.contrib import messages


@login_required
def RegistrarPonto(request):
    context = {}
    context['dataHoje'] = data.date.today().strftime("%d / %B")
    context['diaSemana'] = calendar.day_name[data.date.today().weekday()].capitalize()
    user = request.user
    if HistRegistro.objects.filter(userReg = user.id):
        context['histRegistro'] = HistRegistro.objects.get(userReg = user.id)
        # context = {'histRegistro' : histRegistro} # Processo acima efetua o mesmo que o de baixo

    if request.method == 'POST':
        ha = hora.now().time()

        horaEntM_soma = (hora.combine(hora.today(), user.escala.horaEntM) + timedelta(minutes=5)).time()
        horaEntM_subtrai = (hora.combine(hora.today(), user.escala.horaEntM) + timedelta(minutes=-5)).time()

        horaSaiM_soma = (hora.combine(hora.today(), user.escala.horaSaiM) + timedelta(minutes=5)).time()
        horaSaiM_subtrai = (hora.combine(hora.today(), user.escala.horaSaiM) + timedelta(minutes=-5)).time()

        horaEntV_soma = (hora.combine(hora.today(), user.escala.horaEntV) + timedelta(minutes=5)).time()
        horaEntV_subtrai = (hora.combine(hora.today(), user.escala.horaEntV) + timedelta(minutes=-5)).time()

        horaSaiV_soma = (hora.combine(hora.today(), user.escala.horaSaiV) + timedelta(minutes=5)).time()
        horaSaiV_subtrai = (hora.combine(hora.today(), user.escala.horaSaiV) + timedelta(minutes=-5)).time()

        print(horaEntM_subtrai)
        print(ha)
        print((horaEntM_subtrai >= ha))
        print((horaSaiV_soma <= ha))
        
        # Verifica se o usuario está dentro da sua escala
        if (horaEntM_subtrai <= ha) and (horaSaiV_soma >= ha) or (horaSaiM_subtrai  <= ha) and (horaSaiM_soma >= ha):

            # Se estiver então verifica se já possui registro
            if HistRegistro.objects.filter(userReg = user.id, escala = user.escala.id, dataReg = data.date.today()):

                if not (horaEntM_soma >= ha) and (horaEntM_subtrai  <= ha):
                    messages.error(request, "Você não pode registrar o ponto")
                    
                print(user.escala.id) 
                print(request.POST.get('horas'))
                # messages.error(request, "Problemas ao registrar ponto")  
                return render(request, 'registraPonto/index.html', context)
            else:
                if user.escala.horaEntM != '':
                    #  Se o usuario tentar entrar 5 minutos antes do seu horario e até 5 minutos depois ele consegue
                    # Escala de entrada 08:00 - 5 = 07:55 for maior ou igual ao horario atual e a escala de entrada 08:00 + 5 = 08:05 for menor ou igual a hora atual ele cria o registro 
                    if (horaEntM_subtrai  >= ha) and (horaEntM_soma <= ha):
                        HistRegistro.objects.create(userReg = user.id, escala = user.escala.id, dataReg = data.date.today(), horaEntM = ha)
                    elif (horaSaiM_subtrai  >= ha) and (horaSaiM_soma <= ha):
                        HistRegistro.objects.create(userReg = user.id, escala = user.escala.id, dataReg = data.date.today(), horaSaiM = ha)
                else:
                    HistRegistro.objects.create(userReg = user.id, escala = user.escala.id, dataReg = data.date.today(), horaEntV = ha)     
        else:
           messages.error(request, "Você está fora da sua escala de trabalho!")
           return render(request, 'registraPonto/index.html', context) 
    else:    
        return render(request, 'registraPonto/index.html', context)
