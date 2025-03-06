import requests
import pandas as pd
pd.set_option('display.max_colwidth', None)
# Configuração da API FIPE v2
API_URL = "https://parallelum.com.br/fipe/api/v2"

# Função para buscar marcas de veículos
def obter_marcas():
    url = f"{API_URL}/cars/brands"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao acessar a API FIPE:", response.status_code)
        return []

# Obtendo marcas disponíveis
marcas = obter_marcas()
df_marcas = pd.DataFrame(marcas)

# Exibir lista de marcas para escolha do usuário
print("\nMarcas disponíveis:")
for index, row in df_marcas.iterrows():
    print(f"{index} - {row['name']}")  # Mostra o índice e o nome da marca

# Usuário escolhe a marca pelo índice
indice_marca = int(input("\nDigite o número da marca desejada: "))
codigo_marca = df_marcas.iloc[indice_marca]["code"]

# Exibir a marca escolhida
print(f"\nMarca escolhida: {df_marcas.iloc[indice_marca]['name']}")

# Função para obter modelos da marca escolhida
def obter_modelos(codigo_marca):
    url = f"{API_URL}/cars/brands/{codigo_marca}/models"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao acessar modelos da marca {codigo_marca}: {response.status_code}")
        return []

# Obtendo modelos da marca escolhida
modelos = obter_modelos(codigo_marca)
df_modelos = pd.DataFrame(modelos)

# Exibir modelos para escolha do usuário
print("\nModelos disponíveis:")
for index, row in df_modelos.iterrows():
    print(f"{index} - {row['name']}")  # Mostra o índice e o nome do modelo

# Usuário escolhe o modelo pelo índice
indice_modelo = int(input("\nDigite o número do modelo desejado: "))
codigo_modelo = df_modelos.iloc[indice_modelo]["code"]

# Exibir o modelo escolhido
print(f"\nModelo escolhido: {df_modelos.iloc[indice_modelo]['name']}")

# Função para obter anos disponíveis do modelo escolhido
def obter_anos(codigo_marca, codigo_modelo):
    url = f"{API_URL}/cars/brands/{codigo_marca}/models/{codigo_modelo}/years"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao acessar anos do modelo {codigo_modelo}: {response.status_code}")
        return []

# Obtendo anos do modelo escolhido
anos = obter_anos(codigo_marca, codigo_modelo)
df_anos = pd.DataFrame(anos)

# Exibir anos disponíveis para escolha
print("\nAnos disponíveis:")
for index, row in df_anos.iterrows():
    print(f"{index} - {row['name']}")  # Mostra o índice e o ano

# Usuário escolhe o ano pelo índice
indice_ano = int(input("\nDigite o número do ano desejado: "))
codigo_ano = df_anos.iloc[indice_ano]["code"]

# Exibir o ano escolhido
print(f"\nAno escolhido: {df_anos.iloc[indice_ano]['name']}")

# Função para obter o preço do veículo
def obter_preco(codigo_marca, codigo_modelo, codigo_ano):
    url = f"{API_URL}/cars/brands/{codigo_marca}/models/{codigo_modelo}/years/{codigo_ano}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao acessar preço do veículo {codigo_modelo}: {response.status_code}")
        return None

# Obtendo o preço do veículo escolhido
preco_info = obter_preco(codigo_marca, codigo_modelo, codigo_ano)

# Exibir os dados coletados
print("\n🔹 Informações do veículo escolhido:")
print(preco_info)
# URL base da API do Mercado Livre
ML_API_URL = "https://api.mercadolibre.com/sites/MLB/search"

# Função para buscar anúncios de veículos no Mercado Livre
def buscar_anuncios(modelo):
    params = {
        "q": modelo,  # Nome do modelo do veículo
        "category": "MLB1744",  # Categoria de veículos no Mercado Livre
        "limit": 10  # Número de anúncios a buscar
    }
    
    response = requests.get(ML_API_URL, params=params)

    if response.status_code == 200:
        dados = response.json()
        return dados["results"]  # Retorna a lista de anúncios encontrados
    else:
        print("Erro ao acessar a API do Mercado Livre:", response.status_code)
        return []

# Executando a busca com base no modelo escolhido
anuncios = buscar_anuncios(df_modelos.iloc[indice_modelo]['name'])

# Criando um DataFrame para armazenar os dados
df_anuncios = pd.DataFrame([
    {
        "Título": anuncio["title"],
        "Preço (R$)": anuncio["price"],
        "Ano": anuncio["attributes"][0]["value_name"] if anuncio["attributes"] else "Desconhecido",
        "Localização": anuncio["address"]["state_name"] if "address" in anuncio else "Desconhecido",
        "Link": anuncio["permalink"]
    }
    for anuncio in anuncios
])

# Exibir os dados coletados
print("\n🔹 Anúncios de veículos no Mercado Livre:")
print(df_anuncios)
