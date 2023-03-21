from django.shortcuts import render,redirect
from django.contrib import auth, messages
from .models import User
from django.db.models import Q

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
    return render(request, 'validacao/valida_Email.html')
    