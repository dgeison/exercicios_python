import json
from clima_utils import (
    obter_clima_atual_cidade,
    obter_info_qualidade_ar_cidade,
    obter_info_pais,
)


def classificar_qualidade_ar(aqius):
    if aqius <= 50:
        return "Boa"
    elif aqius <= 100:
        return "Moderada"
    elif aqius <= 150:
        return "Ruim para grupos sensíveis"
    elif aqius <= 200:
        return "Ruim"
    elif aqius <= 300:
        return "Muito ruim"
    else:
        return "Perigosa"


def mostrar_info_cidades():
    cidade = input("Digite o nome da cidade: ")

    clima = obter_clima_atual_cidade(cidade)
    if clima and "current" in clima:
        atual = clima["current"]
        print(f"\nClima em {cidade}:")
        print(f"  Condição: {atual['condition']['text']}")
        print(
            f"  Temperatura: {atual['temp_c']}°C (Sensação: {atual['feelslike_c']}°C)"
        )
        print(f"  Umidade: {atual['humidity']}%")
        print(f"  Vento: {atual['wind_kph']} km/h {atual['wind_dir']}")
        print(f"  Última atualização: {atual['last_updated']}")
    else:
        print("Não foi possível obter o clima para essa cidade.")

    ar_qualidade = obter_info_qualidade_ar_cidade(cidade)
    if ar_qualidade and ar_qualidade.get("status") == "success":
        try:
            pollution = ar_qualidade["data"]["current"]["pollution"]
            aqius = pollution["aqius"]
            data_medicao = pollution["ts"]
            situacao = classificar_qualidade_ar(aqius)
            pais_nome = ar_qualidade["data"]["country"]
            print(f"\nQualidade do ar em {cidade}:")
            print(f"  Índice AQI (US): {aqius} (Situação: {situacao})")
            print(f"  Poluente principal: {pollution['mainus']}")
            print(f"  Data da medição: {data_medicao}")

            dadosPais = obter_info_pais(pais_nome)
            if dadosPais:
                print(f"\nDados do país {dadosPais['nome']}:")
                print(f"  Nome oficial: {dadosPais['nome_oficial']}")
                print(f"  Capital: {dadosPais['capital']}")
                print(f"  População: {dadosPais['populacao']:,}")
                print(f"  Área: {dadosPais['area_km2']:,} km²")
                print(f"  Moeda: {dadosPais['moeda']}")
                print(f"  Continente: {dadosPais['continente']}")
                print(f"  Idiomas: {', '.join(dadosPais['idiomas'])}")
                print(f"  Bandeira: {dadosPais['bandeira']}")
            else:
                print("Não foi possível obter os dados do país.")
        except (KeyError, TypeError):
            print("Não foi possível interpretar a qualidade do ar para essa cidade.")
    else:
        print("Não foi possível obter a qualidade do ar para essa cidade.")


def main():
    mostrar_info_cidades()


if __name__ == "__main__":
    main()
