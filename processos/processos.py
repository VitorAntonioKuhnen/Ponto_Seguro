import random
from accounts.models import Users, Token
from django.contrib.auth.hashers import make_password

from io import BytesIO
from unittest import result
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.template.loader import render_to_string


def geradorToken(usuario):
    user = Users.objects.get(id=usuario)
    if Token.objects.filter(usuario=user.id).exists():
        Token.objects.get(usuario=user.id).delete()
    numbers = [0,1,2,3,4,5,6,7,8,9]
    resultado = ''
    for i in range(6):
        resultado +=  str(random.choice(numbers))
    Token.objects.create(codToken= make_password(resultado), usuario_id=usuario) 
    # Token.objects.create(codToken=resultado, usuario_id=usuario) 
    return resultado


def geraHtmlToPdf(TemplateHtml, context_dict={}):
    template = get_template(TemplateHtml)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None