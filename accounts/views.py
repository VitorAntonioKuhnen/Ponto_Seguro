from django.shortcuts import render,redirect
from django.contrib import auth, messages
from .models import User
from .forms import FormWithCaptcha
from processos import processos
from django.conf import settings
import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def login(request):
    if "login" in request.POST:
        matricula = request.POST.get('matricula')
        senha = request.POST.get('senha')
        if matricula.isdigit():
            username = User.objects.get(matricula=matricula)
            if username != '':
                if username.dt_troca_senha != datetime.date.today():
                    check = auth.authenticate(request, username=username, password=senha)
                    if check is not None:
                        auth.login(request, check)
                        return render(request, 'login/login.html')
                    else:
                        messages.error(request, 'Usuario ou Senha Invalidas!!')
                        return redirect(login) 
                else:
                    return render(request, 'validacao/valida_Email.html')   
            else:
                messages.error(request, 'Usuario ou Senha Invalidas!!')
                return redirect(login)   
        else:
            messages.error(request, 'Usuario ou Senha Invalidas!!')
            return redirect(login)           
    else:
        return render(request, 'login/login.html')
    
def validacao(request):
    form = FormWithCaptcha() 
    if "validaSenha" in request.POST:
        email = request.POST.get('email')
        print(email)
        if email != '': 
            form = FormWithCaptcha(request.POST)
            if form.is_valid():
                validEmail = User.objects.get(email=email)
                if validEmail is None:
                    messages.error(request, 'Informe um Email Válido!')
                    return(redirect, validacao) 
                  
                else:
                    enviaEmail(validEmail.email, processos.geradorToken(validEmail.id))
                    return render(request, 'validacao/valida_Email.html',  {'form': form}) 
            else:
                test = messages.get_messages(request)
                print(test)
                messages.error(request, 'Selecione o reCAPTCHA!')
        else:
            messages.error(request, 'Informe um Email!')  
            test = messages.get_messages(request)
            print(test) 
        return render(request, 'validacao/valida_Email.html',  {'form': form})           
    else:
        print('entrou no primeiro else')          
        return render(request, 'validacao/valida_Email.html',  {'form': form})


def enviaEmail(email, token):
    html_content = render_to_string('email/token.html', {'token': token})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives('PontoSeguro - Token de Identificação', text_content, settings.EMAIL_HOST_USER, [email])
    email.attach_alternative(html_content, 'text/html')
    email.send()
    return "enviado"