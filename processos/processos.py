import random
from accounts.models import User, Token

#Import do Envio de E-mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decouple import config


def enviaEmail(email, titulo, conteudo):
    #Coloque o E-mail e a Senha
    receiver_address = email #Email de destino
    #Configurar o MIME
    message = MIMEMultipart()
    message['From'] = config('Email')#sender_address   Coloque seu E-mail de origem
    message['To'] = config('SenhaApp')#receiver_address   Coloque seu Acesso de App (senha de acesso ao App)
    message['Subject'] = titulo   #Titulo do E-mail

    mail_content = conteudo

    #O corpo e os anexos para o correio
    message.attach(MIMEText(mail_content, 'text/html')) #Plain para enviar apenas o conteudo, e HTML para enviar um e-mail com HTML

    #Criar sessão SMTP para enviar o e-mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #Usar gmail com porta
    session.starttls() #habilitar segurança
    session.login(config('Email'), config('SenhaApp')) #Faça o login com mail_id e senha
    text = message.as_string()
    session.sendmail(config('Email'), receiver_address, text)
    session.quit()
    return 'Email Enviado'


def geradorToken(usuario):
    user = User.objects.get(id=usuario)
    numbers = [0,1,2,3,4,5,6,7,8,9]
    resultado = ''
    for i in range(6):
        resultado +=  str(random.choice(numbers))
    Token.objects.create(codToken=resultado, usuario_id=usuario) 
    return resultado