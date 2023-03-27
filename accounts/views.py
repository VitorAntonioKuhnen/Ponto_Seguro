from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import auth, messages
from .models import User
from .models import Token
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
        if email != '': 
            form = FormWithCaptcha(request.POST)
            if form.is_valid():
                validEmail = User.objects.get(email=email) #Revisar processo de busca de e-mail!!
                print(validEmail)
                print(validEmail.email)
                print(validEmail != '')
                if validEmail != '':
                    print('entrou aqui')
                    enviaEmail(validEmail.email, processos.geradorToken(validEmail.id))
                    url = reverse('token', args=[validEmail.id])
                    return redirect(url)
                else:
                    messages.error(request, 'Informe um Email Válido!')
            else:
                test = messages.get_messages(request)
                messages.error(request, 'Selecione o reCAPTCHA!')
        else:
            messages.error(request, 'Informe um Email!')  
            test = messages.get_messages(request)
        return render(request, 'validacao/valida_Email.html',  {'form': form})           
    else:
        print('entrou no primeiro else')          
        return render(request, 'validacao/valida_Email.html',  {'form': form})

def token(request, id):
    print(id)
    if "verificar" in request.POST:
        codtoken = request.POST.get('codToken')
        if codtoken != '':
            tokenConfirm = Token.objects.filter(usuario=id, codToken=codtoken) 
            print(tokenConfirm)
            print(tokenConfirm.exists())
            if tokenConfirm.exists():
                print('Token Correto!')
                return render(request, 'token/token.html', {'matricula': id})
            else:
                print('Token Invalido')
        return render(request, 'token/token.html', {'matricula': id})
    return render(request, 'token/token.html', {'matricula': id})

# Precisa ser revisado pois dá erro ao efetuar o envio da mensagem pois não tem um retorno como deveria na tela
def gerarToken(request, id):
    usuario = User.objects.get(id=id)
    enviaEmail(usuario.email, processos.geradorToken(usuario.id))
    return render(request, 'token/token.html', {'matricula': id})



def enviaEmail(email, token):
    html_content = render_to_string('email/token.html', {'token': token})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives('PontoSeguro - Token de Identificação', text_content, settings.EMAIL_HOST_USER, [email])
    email.attach_alternative(html_content, 'text/html')
    email.send()
    return "enviado"