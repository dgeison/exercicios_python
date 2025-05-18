import requests
import os
import json
from dotenv import load_dotenv

WEATHER_KEY = os.getenv("WEATHER_KEY")
AIRVISUAL_KEY = os.getenv("AIRVISUAL_KEY")

load_dotenv()


def obter_clima_atual_cidade(cidade):
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


def obter_info_qualidade_ar_cidade(cidade):
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
    

    # Primeiro, descobre estado e país usando a WeatherAPI
    try:
        url_weather = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_KEY}&q={cidade}"
        resposta_weather = requests.get(url_weather)
        resposta_weather.raise_for_status()
        dados_weather = resposta_weather.json()
        location = dados_weather.get("location", {})
        nome_cidade = location.get("name")
        estado = location.get("region")
        if estado and estado == "Distrito Federal":
            estado = "Federal District"
        pais = location.get("country")
        if pais and pais == "brasil":
            pais = "Brazil"
        if not (nome_cidade and estado and pais):
            print("Não foi possível identificar cidade, estado ou país.")
            return None
    except Exception as e:
        print(f"Erro ao identificar estado e país: {e}")
        return None

    # Agora consulta a AirVisual com os dados corretos
    try:
        url = (
            f"http://api.airvisual.com/v2/city"
            f"?city={nome_cidade}&state={estado}&country={pais}&key={AIRVISUAL_KEY}"
        )
        resposta = requests.get(url)
        resposta.raise_for_status()
        return resposta.json()
    except Exception as e:
        print(f"Erro ao consultar a qualidade do ar: {e}")
        return None


def obter_info_pais(pais):
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
            if pais_info.get("name", {}).get("common", "").lower() == pais.lower():
                # Monta um dicionário só com os dados mais importantes
                return {
                    "nome": pais_info.get("name", {}).get("common", "N/A"),
                    "nome_oficial": pais_info.get("name", {}).get("official", "N/A"),
                    "capital": pais_info.get("capital", ["N/A"])[0],
                    "populacao": pais_info.get("population", "N/A"),
                    "area_km2": pais_info.get("area", "N/A"),
                    "moeda": list(pais_info.get("currencies", {}).values())[0].get("name", "N/A") if pais_info.get("currencies") else "N/A",
                    "bandeira": pais_info.get("flags", {}).get("png", "N/A"),
                    "continente": pais_info.get("continents", ["N/A"])[0],
                    "idiomas": list(pais_info.get("languages", {}).values()) if pais_info.get("languages") else ["N/A"]
                }
        print(f"País '{pais}' não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao consultar a API: {e}")
        return None


