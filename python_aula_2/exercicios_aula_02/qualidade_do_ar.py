import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do .env

AIRVISUAL_KEY = os.getenv("AIRVISUAL_KEY")
print(f"AIRVISUAL_KEY carregada: {AIRVISUAL_KEY}")


def listar_paises_dados_qualidade_ar():
    """
    Consulta a lista de países disponíveis na AirVisual API para dados de qualidade do ar.

    Returns:
        list: Uma lista de dicionários contendo os dados dos países retornados pela API,
              caso a consulta seja bem-sucedida.
        None: Retorna None se ocorrer um erro durante a consulta.

    Raises:
        requests.exceptions.RequestException: Caso ocorra um erro na requisição HTTP.
    """
    if not AIRVISUAL_KEY:
        print("Erro: AIRVISUAL_KEY não definida nas variáveis de ambiente.")
        return None
    try:
        url = f"https://api.airvisual.com/v2/countries?key={AIRVISUAL_KEY}"
        resposta = requests.get(url)
        resposta.raise_for_status()
        return resposta.json()
    except Exception as e:
        print(f"Erro ao consultar a API: {e}")
        return None


print(json.dumps(listar_paises_dados_qualidade_ar(), indent=4, ensure_ascii=False))
