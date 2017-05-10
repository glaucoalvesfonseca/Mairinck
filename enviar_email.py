import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email(assunto, remetente, destinatario, mensagem, anexo=False, nome_anexo='Anexo'):
    """
    Função para envio de e-mails com ou sem anexo.
    
    A função enviar_email utiliza seis parâmetros e, após passados pelo usuário, a função montará o e-mail e enviará para o destinatário. As bibliotecas, MIMEBase e encoders só serão importadas se o argumento anexo tiver um valor diferente de False.

    Argumentos:
    
    Assunto: string. Assunto a ser enviado no e-mail;
    Remetente: string. Nome do remetente. Não precisa ser o e-mail;
    Destinatário: string. E-mail do destinatário;
    Mensagem: string. Mensagem a ser enviada no corpo do e-mail;
    Anexo: string. Caminho para acesso ao arquivo que será enviado em anexo;
    Nome_anexo: string. O usuário pode especificar um nome personalizado para o anexo. Por padrão, o nome será Anexo.

    """
    #Preparando dados do e-mail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('arobotwithoutsarcasm@gmail.com', "machineonetwo")
    
    msg = MIMEMultipart()
    msg['Subject'] = assunto
    msg['FROM'] = remetente
    msg['To'] = destinatario

    #Verifica se deseja enviar anexo
    if anexo:
        from email.mime.base import MIMEBase
        from email import encoders
        
        msg.attach(MIMEText(mensagem))
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(anexo, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="{}"'.format(nome_anexo))
        msg.attach(part)

    #Enviando e-mail
    server.sendmail('TARS', destinatario, msg.as_string().encode('ascii'))
    server.quit()