### BIBLIOTECAS
 # Importando a bilioteca pandas (pip install pandas)
import pandas as pd
import requests
import json

### VARIÁVEIS
sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'



### FASE 1 - EXTRAÇÃO DOS DADOS
dataframe = pd.read_csv('SDW2023.csv') # dataframe lerá as infos doa rquivo csv
user_ids = dataframe['UserID'].tolist() # importando os dados na coluna UserID do csv para uma lista

def get_user(id):
  response = requests.get(f'{sdw2023_api_url}/users/{id}')
  return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]



### FASE 2 -TRANSFORMAÇÃO DE DADOS (INTEGRANDO COM IA DO GOOGLE BARD)

# Instalando a biblioteca do API do Google Bard
    # pip install bardapi (dar este comando no terminal python)

# Importando o API do Bard e Key >>> Mais detalhes: https://web.dio.me/topics/ia-alternativa-para-explorando-ia-generativa-em-um-pipeline-de-etl-com-python?back=%2Ftrack%2Fsantander-bootcamp-2023-ciencia-de-dados-com-python&order=undefined&page=1&search=Pipeline&tab=forum&track_id=71477949-f762-43c6-9bf2-9cf3d7f61d4a
from bardapi import Bard
import os
os.environ['_BARD_API_KEY']='bQi631ueMB6UCPtuiO3pUbN1lqWSqDl3SIJcowye4q-NlBFdtlF0vkXOAsvcuM4xFH3gsA.'

def generate_ai_news(user):
  input_text = f"Crie uma unica frase para {user['name']} sobre a importância dos investimentos financeiros máximo 99 caracteres"
  bard_output = Bard().get_answer(input_text)['content']
  return bard_output

for user in users:
  news = generate_ai_news(user)
  user['news'].append({
      "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
      "description": news
  })



### FASE 3 - LOAD (CARREGAMENTO)

# Gerando a mensagem automatizada para cada usuário da lista
def update_user(user):
  response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
  return True if response.status_code == 200 else False

# Confirmando se a mensagem foi atualizada ou não
for user in users:
  success = update_user(user)
  print(f"User {user['name']} updated? {success}!")