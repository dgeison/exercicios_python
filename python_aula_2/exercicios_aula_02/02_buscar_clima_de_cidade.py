import requests
import os
import json
from dotenv import load_dotenv

WEATHER_KEY = os.getenv("WEATHER_KEY")

load_dotenv() 

def buscar_clima(cidade):
    """
    Consulta o clima atual de uma cidade utilizando a WeatherAPI.

    Args:
        cidade (str): O nome da cidade para a qual o clima será consultado.

    Returns:
        dict: Um dicionário contendo os dados do clima retornados pela API, 
              caso a consulta seja bem-sucedida.
        None: Retorna None se ocorrer um erro durante a consulta.

    Raises:
        requests.exceptions.RequestException: Caso ocorra um erro na requisição HTTP.
    """
    """Consulta o clima atual de uma cidade na WeatherAPI."""
    if not WEATHER_KEY:
        print("Erro: WEATHER_KEY não definida nas variáveis de ambiente.")
        return None
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_KEY}&q={cidade}"
        resposta = requests.get(url)
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao consultar o clima: {e}")
        return None
    

print(json.dumps(buscar_clima("Belo Horizonte"), indent=4, ensure_ascii=False))