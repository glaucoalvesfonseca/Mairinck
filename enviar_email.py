import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email(assunto, remetente, destinatario, mensagem, anexo=False):
    
    #Enviando o email 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('arobotwithoutsarcasm@gmail.com', "machineonetwo")
    
    msg = MIMEText(mensagem)
    msg['Subject'] = assunto
    msg['FROM'] = remetente
    msg['To'] = destinatario

    #Verifica se deseja enviar anexo
    if anexo == False:
        pass
    else:
        msg.attach(MIMEMultipart(anexo))

    #Enviando e-mail
    server.sendmail('TARS', destinatario, msg.as_string().encode('ascii'))
    server.quit()

assunto = 'Teste'
remetente = 'TARS'
destinatario = 'pvasconcellos@araruama.unimed.com.br'
mensagem = 'Mensagem de teste'
anexo = os.path.abspath(os.path.dirname(__file__) + '\\teste.txt')

enviar_email(assunto, remetente, destinatario, mensagem, anexo=anexo)
