#Import do Envio de E-mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def enviaEmail(email, titulo, conteudo):
    #Coloque o E-mail e a Senha
    sender_address = 'admenvmail@gmail.com' #'Coloque seu E-mail de origem'
    sender_pass = 'Senha App' #'Coloque seu Acesso de App (senha de acesso ao App)'
    receiver_address = email #Email de destino
    #Configurar o MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = titulo   #Titulo do E-mail

    mail_content = conteudo

    #O corpo e os anexos para o correio
    message.attach(MIMEText(mail_content, 'plain'))
    #Criar sessão SMTP para enviar o e-mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #Usar gmail com porta
    session.starttls() #habilitar segurança
    session.login(sender_address, sender_pass) #Faça o login com mail_id e senha
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    return 'Email Enviado'
