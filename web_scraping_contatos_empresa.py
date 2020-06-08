# -*- coding: cp1252 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas

driver = webdriver.Chrome()  #Abre uma página no Chrome
driver.maximize_window()  #Maximiza a página
driver.get('https://dcc.com/our-people/') #Acessa a url

ver = True
list = []  # Armazena os dados em uma lista
for pag in range(2, 7, 1): #Acessa todas as páginas c/ contatos da empresa

    i = 1 #Seleciona o 1º contato
    while i <= 50:
        button_city = (By.XPATH, '//*[@id="app"]/main/section[2]/div/div/div/div/div/div[1]/select/option[{}]'.format(pag))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(button_city)).click() #Aguarda carregar o local de atuação da empresa e o seleciona

        try:
            button_person = (By.XPATH, '//*[@id="app"]/main/section[2]/div/div/ul/li[{}]/div/h3/a'.format(i))
            WebDriverWait(driver, 10).until(EC.presence_of_element_located(button_person)).click() #Aguarda carregar os contatos e seleciona:
            if pag == pag: #Se continuar no mesmo local, seleciona o próximo contato
                i += 1
            elif pag != pag: #Se mudar o local, seleciona o 1º contato
                i = 1

            button_show_all = (By.XPATH, '//*[@id="app"]/main/section[1]/div/div/div/div[1]/div/div[2]/div/div[2]/ul/li[last()]/a')
            WebDriverWait(driver, 15).until(EC.presence_of_element_located(button_show_all)).click() #Aguarda carregar o botão "Show All" e seleciona para vizualizar todas as categorias de atuação do contato

            soup = BeautifulSoup(driver.page_source, 'html.parser') #Transforma o texto em html
            infos = soup.find_all(class_='person-header__head') #Seleciona a área que contém os dados solicitados

            for info in infos:

                name = info.find('h2')
                name = name.text #Coleta o nome do contato

                email = info.find('a', title='Email')
                email = email.get('href') #Coleta o email do contato

                tags = soup.find_all('a', 'span', class_='btn current')
                all_tags = [] #Cria uma lista de categorias de atuação
                for tag in tags:
                    tag_list = tag.text #Coleta cada categoria do contato
                    all_tags.append(tag_list) #Adiciona cada categoria na lista

                phone1 = True #Se é fornecido o telefone do contato, coleta o telefone
                try:
                    phone = info.find('a', title='Phone')
                    phone = phone.get('href')

                except AttributeError: #Se não é fornecido o telefone do contato, o campo é preenchido com a mensagem "Sem telefone"
                    phone1 = False
                    phone = 'Sem telefone'

            driver2 = webdriver.Chrome() #Abre uma 2ª janela no Chrome
            if (pag == 2):
                driver2.get('https://dcc.com/locations/brisbane/') #Acessa a url conforme o local antes acessado
            elif (pag == 3):
                driver2.get('https://dcc.com/locations/melbourne/')
            elif (pag == 4):
                driver2.get('https://dcc.com/locations/new-zealand/')
            elif (pag == 5):
                driver2.get('https://dcc.com/locations/singapore/')
            else:
                driver2.get('https://dcc.com/locations/sydney/')

            info_location = (By.XPATH, '//*[@id="app"]/main/section[1]/div[1]/div/div[1]/div')
            WebDriverWait(driver2, 10).until(EC.presence_of_element_located((info_location))) #Aguarda carregar a área com dados de localização

            soup2 = BeautifulSoup(driver2.page_source, 'html.parser')  #Transforma o texto em html
            infos2 = soup2.find_all(class_='location-map__info')  #Seleciona a área da página que contém os dados solicitados

            for person_infos2 in infos2:
                city = person_infos2.find('h2', 'span', class_='component-header')
                city = city.text #Coleta a cidade que trabalha o contato

                address = person_infos2.find('p')
                address = address.text.replace('\n', ' ') #Coleta o endereço de trabalho do contato

                list.append({  # Adiciona os dados do contato em um dicionário
                    'Name ': name,
                    'Email': email,
                    'Phone ': phone,
                    'Location ': city + ' ' + address,
                    'Tags ': all_tags
                })

            driver2.close() #Fecha a 2ª página
            driver.back() #Volta a 1ª página p/ a tela inicial

        except: #Se não tiver mais nenhum contato em um local, acessa outro local
            Ver = False
            break

    print(list) #Mostra os dados de cada contato
    df = pandas.DataFrame(list) #Cria um dataframe/tabela
    df.to_csv('Dados_Contatos.csv', index=False) #Salva todos os contatos em um arquivo csv

driver.close() #Fecha a 1ª página