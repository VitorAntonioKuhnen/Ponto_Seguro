import random
from accounts.models import Users, Token
from home.models import HistRegistro, HoraExtra, Justificativa
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from datetime import datetime as data, datetime as hora

import base64

from io import BytesIO
# from unittest import result
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
# from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

from django.conf import settings

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def geradorToken(usuario):
    user = Users.objects.get(id=usuario)
    if Token.objects.filter(usuario=user.id).exists():
        Token.objects.get(usuario=user.id).delete()
    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    resultado = ''
    for i in range(6):
        resultado += str(random.choice(numbers))
    print(resultado)

    Token.objects.create(codToken=make_password(resultado), usuario_id=usuario)
    # Token.objects.create(codToken=resultado, usuario_id=usuario)
    return resultado


def geraHtmlToPdf(TemplateHtml, context_dict={}):
    template = get_template(TemplateHtml)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return base64.b64encode(result.getvalue()).decode('utf-8')
    return None


def gravaJustificativa(request, user):
    print("Este method é De envio de justificativa")
    tipoJust = request.POST.get('tipoJust')
    txtJust = request.POST.get('txtJust').strip()
    print(tipoJust)
    print(txtJust)
    if (tipoJust is None):
        messages.error(request, 'Informe um tipo de Justificativa!')
        return False
    elif (txtJust == ''):
        messages.error(request, 'Digite o Motivo do Atraso!')
        return False

    else:
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

        if HistRegistro.objects.filter(userReg=user.id,  escala_id=user.escala.id, dataReg=data.today().date()):
            histRegistro = HistRegistro.objects.get(
                userReg=user.id,  escala_id=user.escala.id, dataReg=data.today().date())
            just_criada = Justificativa.objects.create(
                txtJust=txtJust, tipoJust_id=tipoJust, data=data.today(), hora=hora.now().time(), userReg_id=user.id)
            if (histRegistro.horSai4 == None) and (diaSemana == True):
                print('dia comum')
                histRegistro.justificativas.add(just_criada)
            else:
                print('hora extra ')
                horaextra = HoraExtra.objects.get(
                    userExtra_id=user.id, dataExtra=data.today().date())
                horaextra.justificativas.add(just_criada)
        else:
            horaextra = HoraExtra.objects.get(
                userExtra_id=user.id, dataExtra=data.today().date())
            just_criada = Justificativa.objects.create(
                txtJust=txtJust, tipoJust_id=tipoJust, data=data.today(), hora=hora.now().time(), userReg_id=user.id)
            print('hora extra ')
            horaextra.justificativas.add(just_criada)

        user.justificar = False
        user.save()
        messages.success(request, 'Justificativa Registrada com Sucesso')
        return True


def enviaEmail(email, situacao, titulo, data, obs, horE1, horS1, horE2, horS2):
    # html_content = render_to_string('email/token.html', {'token': token})
    text_content = strip_tags(f'''
    <div class="card">
      <h1>Atualização do Registro Ponto</h1>
      <p>
        <span class="label">Data do registro:</span>
        <span>{data}</span>
      </p>
      <p>
        <span class="label">Situação:</span>
        <span>{situacao}</span>
      </p>
      <p>
        <h5 class="label">Registros:</h5>
        <table style="border-collapse: collapse; width: 100%; height: 36px;" border="1">
        <tbody>
        <tr style="height: 18px;">
        <td style="width: 25%; height: 18px;">Entrada</td>
        <td style="width: 25%; height: 18px;">Saida</td>
        <td style="width: 25%; height: 18px;">Entrada</td>
        <td style="width: 25%; height: 18px;">Saida</td>
        </tr>
        <tr style="height: 18px;">
        <td style="width: 25%; height: 18px;">{horE1}</td>
        <td style="width: 25%; height: 18px;">{horS1}</td>
        <td style="width: 25%; height: 18px;">{horE2}</td>
        <td style="width: 25%; height: 18px;">{horS2}</td>
        </tr>
        </tbody>
        </table>
      </p>
      <p>
        <span>Observação: {obs}</span>
      </p>
    </div>''')
    email = EmailMultiAlternatives(
        titulo, text_content, settings.EMAIL_HOST_USER, [email])
    email.attach_alternative(f'''<html>
  <head>

  </head>
  <body>
    <div class="card">
      <h1>Confirmação de registro de ponto</h1>
      <p>
        <span class="label">Data do registro:</span>
        <span>{data}</span>
      </p>
      <p>
        <span class="label">Situação:</span>
        <span>{situacao}</span>
      </p>
      <p>
        <h5 class="label">Registros:</h5>
        <table style="border-collapse: collapse; width: 100%; height: 36px;" border="1">
        <tbody>
        <tr style="height: 18px;">
        <td style="width: 25%; height: 18px;">Entrada</td>
        <td style="width: 25%; height: 18px;">Saida</td>
        <td style="width: 25%; height: 18px;">Entrada</td>
        <td style="width: 25%; height: 18px;">Saida</td>
        </tr>
        <tr style="height: 18px;">
        <td style="width: 25%; height: 18px;">{horE1}</td>
        <td style="width: 25%; height: 18px;">{horS1}</td>
        <td style="width: 25%; height: 18px;">{horE2}</td>
        <td style="width: 25%; height: 18px;">{horS2}</td>
        </tr>
        </tbody>
        </table>
      </p>
      <p>
        <span>Observação: {obs}</span>
      </p>
    </div>
  </body>
</html>''', 'text/html')
    email.send()
    return "enviado"




def enviaEmailDivReg(email, contexto):
    html_content = render_to_string('email/divergencia_registro.html', contexto)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives('Divergencia no Registro do Ponto', text_content, settings.EMAIL_HOST_USER, [email])
    email.attach_alternative(html_content, 'text/html')
    email.send()
    return "enviado"