from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import auth, messages
from .models import Users, Token
from home.models import HistRegistro, HoraExtra
from .forms import FormWithCaptcha
from processos import processos
from django.conf import settings
import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
import re
from datetime import datetime as data

from home import views

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Função para continuar logado no site
# def login(request):
#     auth.logout(request)
#     if request.method == 'POST':
#         pass
#     else:
#         return render(request, 'login/index.html')


def login(request):
    if "login" in request.POST:
        auth.logout(request)
        matricula = request.POST.get('matricula')
        senha = request.POST.get('senha')
        if matricula.isdigit():
            if Users.objects.filter(matricula=matricula) != None:
                    username = Users.objects.get(matricula=matricula)
                    if username.check_password(senha):
                        check = auth.authenticate(
                            request, username=username, password=senha)

                        if check is not None:
                            if datetime.date.today() < username.dt_troca_senha:

                                
                                registros = HistRegistro.objects.filter(userReg_id = username.id , dataReg = data.today())
                                if registros:
                                    registro = HistRegistro.objects.get(userReg_id = username.id , dataReg = data.today())
                                    if ((registro.horEnt1 != None) and (registro.horSai2 == None)) or ((registro.horEnt1 != None) and (registro.horSai2 != None) and (registro.horEnt3 != None) and (registro.horSai4 == None)) :
                                        auth.login(request, check)
                                        return redirect(views.inicio)
                                    
                                    # elif ((registro.horSai2 != None and username.escala.horSai4 == None)):
                                    #     messages.warning(request, 'Você não pode mais registrar Pontos hoje!')
                                    #     return redirect(login)

                                    else:
                                        horExtras =  HoraExtra.objects.filter(userExtra_id = username.id, dataExtra=data.today().date())
                                        if horExtras:
                                            horExtra = HoraExtra.objects.get(userExtra_id = username.id, dataExtra=data.today().date())
                                            if ((horExtra.horEnt1 != None) and (horExtra.horSai2 == None)) or ((horExtra.horEnt1 != None) and (horExtra.horSai2 != None) and (horExtra.horEnt3 != None) and (horExtra.horSai4 == None)) :
                                                auth.login(request, check)
                                                return redirect(views.inicio)
                                            elif ((horExtra.horSai4 != None)):
                                                messages.warning(request, 'Você não pode mais registrar Pontos hoje!')
                                                return redirect(login)
                                            else:
                                                auth.login(request, check)
                                                return redirect(views.RegistrarPonto)   
                                        else:  
                                            auth.login(request, check)
                                            return redirect(views.RegistrarPonto)     
                                else:
                                        horExtras =  HoraExtra.objects.filter(userExtra_id = username.id, dataExtra=data.today().date())
                                        if horExtras:
                                            horExtra = HoraExtra.objects.get(userExtra_id = username.id, dataExtra=data.today().date())
                                            if ((horExtra.horEnt1 != None) and (horExtra.horSai2 == None)) or ((horExtra.horEnt1 != None) and (horExtra.horSai2 != None) and (horExtra.horEnt3 != None) and (horExtra.horSai4 == None)) :
                                                auth.login(request, check)
                                                return redirect(views.inicio)
                                            
                                            elif((horExtra.horSai4 != None)):
                                                auth.logout(request)
                                                print(horExtra.horSai2 != None)
                                                print(username.escala.horSai4 == None)
                                                print(horExtra.horSai4 != None)
                                                messages.warning(request, 'Você não pode mais registrar Pontos hoje!')
                                                return redirect(login)
                                            else:
                                                auth.login(request, check)
                                                return redirect(views.RegistrarPonto)   
                                        else:  
                                            auth.login(request, check)
                                            return redirect(views.RegistrarPonto)    
                            else:
                                url = reverse('trocaSenha', args=[username.id])
                                return redirect(url)
                        else:
                            messages.error(request, 'Usuario ou Senha Invalidas!!')
                            return redirect(login)  
                    else:
                        messages.error(request, 'Usuario ou Senha Invalidas!!')
                        return redirect(login)      
            else:
                messages.error(request, 'Usuario ou Senha Invalidas!!')
                return redirect(login)   
        else:
            messages.error(request, 'Usuario ou Senha Invalidas!!')
            return redirect(login)           
    else:
        return render(request, 'login/login.html')
    


def validacao(request):
    email = request.POST.get('email')
    email = ''
    form = FormWithCaptcha() 
    if request.method == 'POST':
        email = request.POST.get('email').strip()
        if email != '': 
            form = FormWithCaptcha(request.POST)
            if form.is_valid():
                if Users.objects.filter(email=email):
                    validEmail = Users.objects.get(email=email)
                    print('entrou aqui')
                    enviaEmail(validEmail.email, processos.geradorToken(validEmail.id))
                    url = reverse('token', args=[validEmail.id])
                    return redirect(url)
                else:
                    messages.error(request, 'Informe um Email Válido!')
            else:
                messages.error(request, 'Selecione o reCAPTCHA!')
        else:
            messages.error(request, 'Informe um Email!')  
        return render(request, 'validacao/valida_Email.html',  {'form': form})           
    else:
        print('entrou no primeiro else')          
        return render(request, 'validacao/valida_Email.html',  {'form': form})



def token(request, id):
    if request.method == 'POST':
        codtoken = request.POST.get('codToken').strip()

        if codtoken != '':
            if Token.objects.filter(usuario=id).exists:
                if check_password(codtoken, Token.objects.get(usuario=id).codToken):
                    print('Token Correto!')
                    url = reverse('trocaSenha', args=[id])
                    return redirect(url)
                else:
                        messages.error(request, 'Informe um TOKEN Válido!') 
                        print('Token Invalido!')        
            else:
                    messages.error(request, 'Informe um TOKEN Válido!') 
                    print('Informe um TOKEN Válido!')        
        else:
                messages.error(request, 'Informe um TOKEN para continuar') 
                print('Informe um TOKEN para continuar')        
                    
        return render(request, 'token/token.html', {'userId': id})
    if Token.objects.filter(usuario=id).exists():
        return render(request, 'token/token.html', {'userId': id})
    else:
        messages.error(request, 'Você não possui TOKENS para confirmar')
        return redirect(validacao)



# Precisa ser revisado pois dá para acessar diretamente pelo link
def gerarToken(request, id):
    if Token.objects.filter(usuario=id).exists():
        print('Entrou Gerando novo Token')
        if Token.objects.filter(usuario=id).exists():
            Token.objects.get(usuario=id).delete()   
        usuario = Users.objects.get(id=id)
        enviaEmail(usuario.email, processos.geradorToken(usuario.id))
        return HttpResponse('''<div class="alert alert-success alert-dismissible fade show" id="mensagem" role="alert">
                    <p>Seu novo Token foi Regerado! Confira seu e-mail</p>
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>''')
    else:
        messages.error(request, "Você não possui acesso a está função!")
        return redirect(validacao)



def cancelaTk(request, id):
    if Token.objects.filter(usuario=id).exists():
            Token.objects.get(usuario=id).delete()
    messages.success(request, 'Token cancelado com sucesso!')    
    return redirect(validacao)        



def trocaSenha(request, id):
    if request.method == 'POST':
        print('entrou')
        senha1 = request.POST.get('senha1')
        senha2 = request.POST.get('senha2')
        if senha1 == senha2 and senha1 != '' and senha2 != '':
            print('entrou na validação da senha ')
            
            # Verifica se possui no minimo 8 caracteres
            if len(senha1) < 8:
                messages.error(request, 'A senha precisa ter no minimo 8 Caracteres!')  
                return render(request, 'trocaSenha/trocaSenha.html')

            # Verificar se a senha contém letras
            if not re.search(r'[a-zA-Z]', senha1):
                messages.error(request, 'A senha precisa ter Letras!')  
                return render(request, 'trocaSenha/trocaSenha.html')

            # Verificar se a senha contém números
            if not re.search(r'\d', senha1):
                messages.error(request, 'A senha precisa ter Números!')  
                return render(request, 'trocaSenha/trocaSenha.html')

            # Verificar se a senha contém caracteres especiais
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha1):
                messages.error(request, 'A senha precisa ter Caracteres Especiais!')  
                return render(request, 'trocaSenha/trocaSenha.html')
            else:
                print('Trocando a senha')
                usuario = Users.objects.get(id=id)
                usuario.password = make_password(senha1)
                dt_atual = datetime.date.today()
                usuario.dt_troca_senha = dt_atual.replace(month=dt_atual.month + 6)
                usuario.save()
                return redirect(login)

        else:
            messages.error(request, 'Senha digitadas vazias ou não coincidem')  
            return render(request, 'trocaSenha/trocaSenha.html')  
    
    elif Users.objects.filter(id=id):
        if Users.objects.get(id=id).dt_troca_senha <= datetime.date.today() or Token.objects.filter(usuario=id).exists():
            print('Entrou na tela de Troca de Senha')
            if Token.objects.filter(usuario=id).exists():
                Token.objects.get(usuario=id).delete()
            return render(request, 'trocaSenha/trocaSenha.html')
        else:
            print('Não entrou na tela de Troca de Senha')
            messages.error(request, 'Não pode fazer este processo!')
            return redirect(login)
    else:
        print('Não entrou na tela de Troca de Senha')
        messages.error(request, 'Não pode fazer este processo!')
        return redirect(login)



def enviaEmail(email, token):
    html_content = render_to_string('email/token.html', {'token': token})
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives('PontoSeguro - Token de Identificação', text_content, settings.EMAIL_HOST_USER, [email])
    email.attach_alternative(html_content, 'text/html')
    email.send()
    return "enviado"

def logout(request):
    auth.logout(request)
    return redirect('login')