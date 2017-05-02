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

def escolhe_usuario(numero_aleatorio):
    """
    A função escolhe_usuario armazena as credenciais de acesso dos funcionários da TI. A função retorna uma lista para que possa ser utilizada
    pelo script, que selecionará um usuário aleatório para adicionar contatos nas ocorrências
    """
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
    """
    A função acessar_ocorrencias serve apenas para acessar a página de ocorrências pendentes com a Fácil. Ao invés de adicionar essas três linhas
    de código no for loop, foi decidido que era melhor armazená-las em uma função para melhor manutenção e utilização.

    Devido a algum bug no WebCRM, quando o usuário clica em "Pendentes com a Fácil", a página não é carregada. Por esse motivo, a função irá clicar,
    inicialmente, no botão "Consulta Ocorrências", em seguida clicará em "Pendentes com a Fácil" e, novamente, clicará em "Consultar Ocorrências".
    """
    
    driver.find_element_by_name('ctl00$mnuPrincipal$imgConsultaOcorrencias').click()
    driver.find_element_by_id('ctl00_body_Uc_ConsultaOcorrencias_rblStatus_2').click()
    driver.find_element_by_name('ctl00$mnuPrincipal$imgConsultaOcorrencias').click()

def encontre_ocorrencia():
    """
    A função encontre_ocorrencia servirá para localizar a devida ocorrência para adicionar o contato. Ela será utilizada no for loop após algumas condições serem atendidas. A função não retorna nenhum valor, mas, ao final, chama a ocorrência adicionar_contato para inclusão da mensagem.

    A função está ligada ao logging e, caso encontre a ocorrência em questão, irá chamar a função adicionar_contato, caso contrário, informará no 
    log que tal chamado não existe.
    """
    #Verifica se a ocorrência existe
    if driver.find_element_by_xpath('//*[@id="ctl00_body_Uc_ConsultaOcorrencias_dgOcorrencias_ctl{0:02d}_lnkDetalhe"]'.format(i)):
        ocorrencia = driver.find_element_by_xpath('//*[@id="ctl00_body_Uc_ConsultaOcorrencias_dgOcorrencias_ctl{0:02d}_lnkDetalhe"]'.format(i))
        logging.info('================================== ADICIONANDO CONTATO NA OCORRÊNCIA {} =================================='.format(ocorrencia.text))
        #Abrindo ocorrência
        ocorrencia.click()
        #Adicionando contato
        adicionar_contato()
    else:
        #Caso não ache a ocorrência, adiciona a seguinte mensagem no log
        logging.info('================================== OCORRÊNCIA NÃO EXISTE ==================================')

def adicionar_contato():
    """
    A função adicionar_contato irá adicionar uma mensagem aleatória (definida dentro da variável mensagem_aleatoria). Inicialmente, a função irá verificar se há, pelo menos, um dia de janela de tempo entre o último contato e o momento atual. Se o último contato foi adicionado há mais de um dia, ele segue e adiciona um contato de cobrança, caso contrário, ele não faz nada e segue para a próxima ocorrência.
    """
    #Verifica a data do último contato no chamado
    data_ultimo_contato = driver.find_element_by_xpath('//*[@id="ctl00_body_uc_ContatosOcorrencia_dgContatosOcorrencia"]/tbody/tr[2]/td[2]').text
    #Convertendo a data para datetime
    data_ultimo_contato = datetime.strptime(data_ultimo_contato, '%d/%m/%Y %H:%M')
    #Tempo entre o último contato e hoje
    data_ultimo_contato = int((hoje - data_ultimo_contato).total_seconds())    
    print(hoje.day)
    
    #Verifica se hoje é segunda-feira. Se for, o script verificará se o último contato tem pelo menos 3 dias
    if hoje.day == 2:
        if data_ultimo_contato >= 259200:
            #Aguardar x segundos antes de dar o contato
            time.sleep(random.choice(range(0,20)))
            #Localizando campo de contato
            formulario_de_contato = driver.find_element_by_name('ctl00$body$uc_ContatosOcorrencia$txtContato')
            #Selecionando uma mensagem aleatória
            formulario_de_contato.send_keys(random.choice(mensagem_aleatoria))
            #Enviando contato
            #--driver.find_element_by_name('ctl00$body$uc_ContatosOcorrencia$btnGravar').click()
            #Voltar a página inicial
            driver.find_element_by_id('ctl00_body_lnkBtnVoltar').click()
            #Adicionando contato ao log
            logging.info('================================== CONTATO ADICIONADO ==================================')
            #Voltando a página inicial
            acessar_ocorrencias()
        else:
            driver.find_element_by_id('ctl00_body_lnkBtnVoltar').click()
            #Voltando a página inicial
            acessar_ocorrencias()
    #Se não for segunda-feira:
    else:
        #Verifica se o último contato foi inserido a pelo menos 24 horas
        if data_ultimo_contato >= 86400:        
            #Aguardar x segundos antes de dar o contato
            time.sleep(random.choice(range(0,20)))
            #Localizando campo de contato
            formulario_de_contato = driver.find_element_by_name('ctl00$body$uc_ContatosOcorrencia$txtContato')
            #Selecionando uma mensagem aleatória
            formulario_de_contato.send_keys(random.choice(mensagem_aleatoria))
            #Enviando contato
            #--driver.find_element_by_name('ctl00$body$uc_ContatosOcorrencia$btnGravar').click()
            #Voltar a página inicial
            driver.find_element_by_id('ctl00_body_lnkBtnVoltar').click()
            #Adicionando contato ao log
            logging.info('================================== CONTATO ADICIONADO ==================================')
            #Voltando a página inicial
            acessar_ocorrencias()
        #Se não encontrar a ocorrência, segue para a próxima
        else:
            driver.find_element_by_id('ctl00_body_lnkBtnVoltar').click()
            #Voltando a página inicial
            acessar_ocorrencias()

#Mensagem aleatória para adicionar nas ocorrências
mensagem_aleatoria = ['Alguma novidade?', 'Alguma novidade quanto a essa ocorrência?', 'Prezados,\nAlguma novidade sobre esta ocorrência?', 'Como está o andamento da ocorrência?', 'Prezados,\nQual o status da ocorrência?', 'Prezados,\nComo está o andamento desta ocorrência?', 'Prezados,\nComo está o andamento desta ocorrência? Podemos ajudar em algo?']

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
