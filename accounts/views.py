from django.shortcuts import render,redirect
from django.contrib import auth, messages
from .models import User
from .forms import FormWithCaptcha
from processos import processos


def login(request):
    if "login" in request.POST:
        matricula = request.POST.get('matricula')
        senha = request.POST.get('senha')
        if matricula.isdigit():
            username = User.objects.get(matricula=matricula)
            if username != '':
                check = auth.authenticate(request, username=username, password=senha)
                if check is not None:
                    auth.login(request, check)
                    return render(request, 'login/login.html')
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
    if request.method == "POST":
        form = FormWithCaptcha(request.POST)
        if form.is_valid():
            # print("reCAPTCHA " + request.POST.get("g-recaptcha-response"))
            email = request.POST.get('email')
            validEmail = User.objects.get(email=email)
            if validEmail is None:
                return(redirect, validacao)   
            else:
                enviaEmail(validEmail.email)
                return render(request, 'validacao/valida_Email.html',  {'form': form}) 
        else:
            messages.error(request, 'Selecione o reCAPTCHA!')
            print("erro aqui ó")
    form = FormWithCaptcha()       
    return render(request, 'validacao/valida_Email.html',  {'form': form})


def enviaEmail(email):

    conteudo =  f'''<div style="display: flex; flex-direction: column; align-items: center; gap: 15px; width: 100%; height: 100%; ">
        <nav style="background: linear-gradient(rgb(93, 224, 230) 0%, rgb(0, 74, 173) 100%); display: flex; flex-direction: column; align-items: center; font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif; padding: 5px 10px;">
            <div style="color: white;">
                <h2>Seu Token para Troca de Senha</h2>
            </div>
            <div style="color: rgb(182, 182, 182);">
                <p>Olá, vimos que solicitou a troca da sua senha, abaixo segue o seu código <b style="color: rgb(255, 255, 255);">TOKEN</b>. Se caso você
                    não tenha feito a solicitação pode desconsiderar este e-mail! </p>
            </div>
        </nav>
        <nav style="display: flex; gap: 1%;">
            <div style="border: 1px solid black; width: 80px; text-align: center;">
                <h1>{1}</h1>
            </div>
            <div style="border: 1px solid black; width: 80px; text-align: center;">
                <h1>{2}</h1>
            </div>
            <div style="border: 1px solid black; width: 80px; text-align: center;">
                <h1>{3}</h1>
            </div>
            <div style="border: 1px solid black; width: 80px; text-align: center;">
                <h1>{4}</h1>
            </div>
            <div style="border: 1px solid black; width: 80px; text-align: center;">
                <h1>{5}</h1>
            </div>
            <div style="border: 1px solid black; width: 80px; text-align: center;">
                <h1>{6}</h1>
            </div>
        </nav>
        <div style="text-align: center; padding-bottom: 1%; position: fixed; bottom: 0;">
            <p>Este e-mail foi enviado através de um processo automático, gentileza não responder!</p>
            <img src="templates\static\image\logo_400x400 ponto seguro de lado.png" alt="" style="width: 200px;">
        </div>

    </div>'''


    processos.enviaEmail(email, 'PontoSeguro - Token de Identificação', conteudo)
    return "enviado"