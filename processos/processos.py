import random
from accounts.models import User, Token
from django.contrib.auth.hashers import make_password


def geradorToken(usuario):
    user = User.objects.get(id=usuario)
    numbers = [0,1,2,3,4,5,6,7,8,9]
    resultado = ''
    for i in range(6):
        resultado +=  str(random.choice(numbers))
    # Token.objects.create(codToken= make_password(resultado), usuario_id=usuario) 
    Token.objects.create(codToken=resultado, usuario_id=usuario) 
    return resultado