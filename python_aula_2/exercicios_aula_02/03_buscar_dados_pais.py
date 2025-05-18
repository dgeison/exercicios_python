import requests
import os
import json
from dotenv import load_dotenv

WEATHER_KEY = os.getenv("WEATHER_KEY")
AIRVISUAL_KEY = os.getenv("AIRVISUAL_KEY")

def buscar_dados_pais(pais):
    """
    Consulta informações sobre um país utilizando a REST Countries API.

    Args:
        pais (str): Nome comum do país (ex: "Brazil", "France").

    Returns:
        dict: Um dicionário contendo os dados do país retornados pela API,
              caso a consulta seja bem-sucedida.
        None: Retorna None se ocorrer um erro durante a consulta.

    Raises:
        requests.exceptions.RequestException: Caso ocorra um erro na requisição HTTP.
    """
    try:
        url_country = "https://restcountries.com/v3.1/all"
        resposta_country = requests.get(url_country)
        resposta_country.raise_for_status()
        lista_paises = resposta_country.json()
        for pais_info in lista_paises:
            # Verifica se o nome comum do país bate (case insensitive)
            if pais_info.get("name", {}).get("common", "").lower() == pais.lower():
                return pais_info
        print(f"País '{pais}' não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao consultar a API: {e}")
        return None
    
resultado = buscar_dados_pais("Brazil")
print(json.dumps(resultado, indent=4, ensure_ascii=False))
