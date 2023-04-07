from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Users

@login_required
def RegistrarPonto(request):
    return render(request, 'registraPonto/index.html')
