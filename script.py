from selenium import webdriver
import time
import random
import logging
from datetime import datetime
import os

#Caminho onde o script está
caminho = os.path.abspath(os.path.dirname(__file__)) + '/'

#Data de hoje
hoje = datetime.today()

#Criando arquivo de log
logging.basicConfig(filename=caminho + '{}-{}-{}.log'.format(hoje.day, hoje.month, hoje.year), filemode='w', level=logging.DEBUG)

#Credenciais dos usuários
def escolhe_usuario(numero_aleatorio):
    if numero_aleatorio == 0:
        credenciais = ['paulo henrique','facil']
    elif numero_aleatorio == 1:
        credenciais = ['esilva','3441663']
    elif numero_aleatorio == 2:
        credenciais = ['paulo victor','facil10']
    elif numero_aleatorio == 3:
        credenciais = ['chrystopher','minhasenha']
    elif numero_aleatorio == 4:
        credenciais = ['glauco','facil']
    return credenciais

#Essa função acessa a página de ocorrências pendentes com a Fácil
def acessar_ocorrencias():
    #Acessando ocorrências pendentes com a Fácil
    driver.find_element_by_name('ctl00$mnuPrincipal$imgConsultaOcorrencias').click()
    driver.find_element_by_id('ctl00_body_Uc_ConsultaOcorrencias_rblStatus_2').click()
    driver.find_element_by_name('ctl00$mnuPrincipal$imgConsultaOcorrencias').click()

#Função para encontrar a respectiva ocorrência
def encontre_ocorrencia():
    #Verifica se a ocorrência existe
    if driver.find_element_by_xpath('//*[@id="ctl00_body_Uc_ConsultaOcorrencias_dgOcorrencias_ctl{0:02d}_lnkDetalhe"]'.format(i)):
        ocorrencia = driver.find_element_by_xpath('//*[@id="ctl00_body_Uc_ConsultaOcorrencias_dgOcorrencias_ctl{0:02d}_lnkDetalhe"]'.format(i))
        logging.info('================================== ADICIONANDO CONTATO NA OCORRÊNCIA {} =================================='.format(ocorrencia.text))
        #Abrindo ocorrência
        ocorrencia.click()
        adicionar_contato()
    else:
        logging.info('================================== OCORRÊNCIA NÃO EXISTE ==================================')

#Função só funciona dentro do for loop, devido ao nome da variável ocorrencia
def adicionar_contato():
    
    #Verifica a data do último contato no chamado
    data_ultimo_contato = driver.find_element_by_xpath('//*[@id="ctl00_body_uc_ContatosOcorrencia_dgContatosOcorrencia"]/tbody/tr[2]/td[2]').text
    #Convertendo a data para datetime
    data_ultimo_contato = datetime.strptime(data_ultimo_contato, '%d/%m/%Y %H:%M')
    #Tempo entre o último contato e hoje
    data_ultimo_contato = int((hoje - data_ultimo_contato).total_seconds())
    print(data_ultimo_contato)

    #Verifica se o último contato foi inserido a pelo menos um dia
    if data_ultimo_contato > 86400:        
        #Aguardar x segundos antes de dar o contato
        time.sleep(random.choice(range(0,20)))
        #Localizando campo de contato
        formulario_de_contato = driver.find_element_by_name('ctl00$body$uc_ContatosOcorrencia$txtContato')
        #Selecionando uma mensagem aleatória
        formulario_de_contato.send_keys(random.choice(mensagem_aleatoria))
        #enviando contato
        #--driver.find_element_by_name('ctl00$body$uc_ContatosOcorrencia$btnGravar').click()
        #Voltar a página inicial
        driver.find_element_by_id('ctl00_body_lnkBtnVoltar').click()
        logging.info('================================== CONTATO ADICIONADO ==================================')
        acessar_ocorrencias()

mensagem_aleatoria = ['Alguma novidade?', 'Alguma novidade quanto a essa ocorrência?', 'Prezados,\nAlguma novidade sobre esta ocorrência?']

#Iniciando navegador
driver = webdriver.Chrome('C:\Temp\chromedriver.exe')
driver.get('http://crm.facilinformatica.com.br/FACWEBCRM_SITE/')

logging.info('================================== ADICIONANDO USUÁRIO E SENHA ==================================')
#Localizando campos no HTML
empresa = driver.find_element_by_id('idLogin_txtEmpresa')
usuario = driver.find_element_by_id('idLogin_txtLogin')
senha = driver.find_element_by_id('idLogin_txtSenha')

logging.info('================================== LOGANDO NO WEBCRM ==================================')
#Autenticando
usuario_da_vez = escolhe_usuario(random.choice(range(0,5)))

empresa.send_keys('araruama')
usuario.send_keys(usuario_da_vez[0])
senha.send_keys(usuario_da_vez[1])
driver.find_element_by_name('idLogin$btnLogin').click()

#Aguardar cinco segundos antes de continuar
time.sleep(5)

logging.info(' ================================== ACESSANDO OCORRÊNCIAS ==================================')
acessar_ocorrencias()

#Verificando quantas páginas de ocorrência existem utilizando o rodapé "Página X de X"
total_de_paginas = driver.find_element_by_id('ctl00_body_Uc_ConsultaOcorrencias_lblPagina').text.split()

#Criando for loop cada página
for pagina in range(int(total_de_paginas[-1]) + 1):
    for i in range(3, 11):
        try:
            if pagina == 0:
                encontre_ocorrencia()
            else:
                #Acessando página
                driver.find_element_by_xpath('//*[@id="ctl00_body_Uc_ConsultaOcorrencias_dgOcorrencias"]/tbody/tr[10]/td/a[{}]'.format(pagina)).click()
                #Aguardar 10 segundos antes de continuar. As vezes o WebCRM demora para abrir a página
                time.sleep(10)
                encontre_ocorrencia()
        except:
            break
        logging.info('================================== ACESSANDO PÁGINA {} =================================='.format(pagina+1))

#Fechando navegador
logging.info('================================== SCRIPT FINALIZADO ==================================')
driver.close
