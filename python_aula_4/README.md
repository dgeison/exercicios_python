# Resumo Detalhado do Jupyter Notebook: aula4.ipynb

**Título da Aula Prática:** Integração entre PostgreSQL (Pagila) e APIs com Python

**Objetivo Geral da Atividade:**
Este notebook tem como objetivo central capacitar o usuário na integração de dados provenientes de um banco de dados PostgreSQL (o banco de exemplo "Pagila") com informações obtidas em tempo real de diversas APIs externas. A atividade abrange a consulta, combinação, análise, transformação e visualização desses dados heterogêneos, utilizando Python e suas bibliotecas padrão para manipulação e análise de dados.

**Principais Ferramentas e Tecnologias Utilizadas:**
* **Linguagem de Programação:** Python
* **Ambiente de Desenvolvimento:** Jupyter Notebook
* **Banco de Dados:** PostgreSQL (com o banco de dados de exemplo "Pagila")
* **Interação com Banco de Dados:** Biblioteca `psycopg2` para conexão e execução de queries.
* **Manipulação e Análise de Dados:** Biblioteca `pandas` para estruturas de dados (DataFrames) e operações de análise.
* **Requisições a APIs Externas:** Biblioteca `requests` para realizar chamadas HTTP.
* **APIs Externas Específicas:**
    * WeatherAPI (para dados climáticos como temperatura)
    * AirVisual API (IQAir) (para dados de qualidade do ar - AQI)
    * REST Countries API (para dados populacionais e regionais de países)
* **Gerenciamento de Configurações:** Biblioteca `dotenv` para carregar variáveis de ambiente (como chaves de API e credenciais do banco) de um arquivo `.env`.
* **Visualização de Dados:** Bibliotecas `matplotlib` e `seaborn` para a criação de gráficos.
* **Formatação de Saída:** Biblioteca `tabulate` para exibir DataFrames de forma legível no console.
* **Operações Numéricas:** Biblioteca `numpy`.
* **Outras:** Módulo `os` para interagir com o sistema operacional (ex: caminhos de arquivo para cache) e `time` para possíveis delays em chamadas de API.

**Estrutura e Configuração Inicial do Notebook:**

1.  **Importação de Bibliotecas:** Todas as bibliotecas listadas acima são importadas no início.
2.  **Carregamento de Variáveis de Ambiente:** As credenciais do banco de dados (PG\_DB, PG\_USER, etc.) e as chaves das APIs (WEATHER\_API\_KEY, AIRVISUAL\_API\_KEY) são carregadas do arquivo `.env`.
3.  **Conexão com PostgreSQL:** É estabelecida uma conexão com o banco de dados Pagila, e a versão do PostgreSQL é verificada e impressa.
4.  **Funções Utilitárias Principais:**
    * `run_query(sql, db_conn)`: Executa uma consulta SQL no banco de dados conectado e retorna o resultado como um DataFrame Pandas. Inclui tratamento básico de erro.
    * **Funções de Cache (para o Exercício 10):**
        * `carregar_cache_csv(filepath, key_col, value_col)`: Carrega dados de um arquivo CSV para um dicionário em memória, servindo como cache.
        * `salvar_cache_csv(cache_data, filepath, key_name, value_name)`: Salva o conteúdo do cache em memória para um arquivo CSV.
        * `carregar_cache_paises() / salvar_cache_paises()`: Funções específicas para o cache da API REST Countries, que armazena dicionários de dados.
    * **Funções de Busca de Dados de APIs (Integradas com Cache):**
        * `_buscar_clima_api(cidade)` e `buscar_clima(cidade)`: A primeira realiza a chamada à WeatherAPI; a segunda gerencia o cache para os dados de temperatura.
        * `_buscar_aqi_cidade_api(cidade, estado, pais)` e `buscar_aqi_cidade(cidade, estado, pais)`: Similarmente, para a AirVisual API, buscando o AQI.
        * `_buscar_dados_pais_api(nome_pais_api)` e `buscar_dados_pais(nome_pais_pagila)`: Para a REST Countries API, buscando população, região, etc. Inclui um mapa (`country_name_map_rest`) para normalizar nomes de países entre o Pagila e a API.
    * As funções de API incluem um pequeno `time.sleep()` para evitar sobrecarregar os servidores das APIs.

**Resumo Detalhado dos Exercícios:**

* **Exercício 1 – Temperatura Média das Cidades dos Clientes:**
    * **Objetivo:** Calcular a temperatura média das cidades que possuem clientes com mais de 10 transações totais, ponderada pelo número de clientes distintos em cada uma dessas cidades.
    * **Fontes:** Pagila (tabelas `city`, `address`, `customer`, `payment`), WeatherAPI.
    * **Lógica:** Uma consulta SQL obtém as cidades, o número de clientes e o total de transações (para o filtro). Para uma amostra dessas cidades (as 20 com mais clientes), busca-se a temperatura via `buscar_clima()`. A média ponderada da temperatura é calculada usando `num_clientes` como peso.
    * **Saída:** Temperatura média ponderada e listas de cidades (da amostra) com as temperaturas mais altas e mais baixas, e com mais clientes.

* **Exercício 2 – Receita Bruta em Cidades com Clima Ameno:**
    * **Objetivo:** Identificar o faturamento total proveniente de cidades onde a temperatura atual está entre 18°C e 24°C.
    * **Fontes:** Pagila (tabelas `payment`, `customer`, `address`, `city`), WeatherAPI.
    * **Lógica:** Uma consulta SQL calcula a receita bruta por cidade. Para uma amostra dessas cidades (as 30 com maior receita), a temperatura é obtida. Os dados são filtrados pela faixa de temperatura especificada e a receita bruta total dessas cidades é somada.
    * **Saída:** Lista de cidades (amostra) com clima ameno e sua receita, e o faturamento total dessas cidades.

* **Exercício 3 – Aluguel de Filmes por País e População:**
    * **Objetivo:** Calcular o número de aluguéis por 1.000 habitantes para cada país, visando identificar os países proporcionalmente mais "cinéfilos".
    * **Fontes:** Pagila (tabelas `rental`, `customer`, `address`, `city`, `country`), REST Countries API.
    * **Lógica:** Consulta SQL para obter o número total de aluguéis por país. Em seguida, para cada país, a função `buscar_dados_pais()` (com cache) obtém a população. É calculada a métrica de aluguéis por 1.000 habitantes.
    * **Saída:** Ranking dos 5 países mais "cinéfilos" com base na métrica calculada.

* **Exercício 4 – Filmes Mais Populares em Cidades Poluídas:**
    * **Objetivo:** Listar os filmes mais alugados nas 10 cidades com maior número de clientes que também apresentam um Índice de Qualidade do Ar (AQI) superior a 150.
    * **Fontes:** Pagila (tabelas `customer`, `address`, `city`, `country`, `rental`, `inventory`, `film`), AirVisual API.
    * **Lógica:**
        1.  Identificar as 10 cidades com mais clientes (com detalhes de distrito e país).
        2.  Para essas cidades, buscar o AQI usando `buscar_aqi_cidade()` (que utiliza um mapa `country_name_map_airvisual` para adequar nomes de países e heurísticas para o "estado").
        3.  Filtrar as cidades com AQI > 150.
        4.  Para essas cidades poluídas, executar uma nova consulta SQL para encontrar os filmes mais alugados.
    * **Saída:** Listas de filmes populares para cada cidade poluída identificada na amostra, seguida de uma discussão sobre a complexidade de inferir causalidade entre poluição e preferência de filmes.

* **Exercício 5 – Clientes em Áreas Críticas:**
    * **Objetivo:** Identificar clientes que residem em cidades com AQI > 130 e apresentar um perfil combinado (nome, cidade, país, temperatura, AQI), classificando-os como "zona de atenção ambiental".
    * **Fontes:** Pagila (clientes, localização), AirVisual API, WeatherAPI.
    * **Lógica:** Obter uma lista de cidades distintas dos clientes. Para uma amostra de 50 dessas cidades, buscar o AQI e a temperatura. Filtrar as cidades com AQI > 130. Em seguida, buscar os clientes que residem nessas cidades críticas e combinar os dados.
    * **Saída:** Se encontradas, lista de cidades críticas e, subsequentemente, uma tabela com os clientes dessas áreas e seus dados ambientais. (Na execução de exemplo, nenhuma cidade na amostra atingiu o critério de AQI).

* **Exercício 6 – Receita por Continente:**
    * **Objetivo:** Calcular e visualizar a distribuição da receita total da locadora por continente.
    * **Fontes:** Pagila (pagamentos, localização), REST Countries API.
    * **Lógica:** Consulta SQL para obter a receita total por país. Usar `buscar_dados_pais()` para obter a região (continente) de cada país. Agrupar a receita por região e calcular a soma.
    * **Saída:** Tabela com a receita total por continente e um gráfico de pizza (`matplotlib`) mostrando essa distribuição.

* **Exercício 7 – Tempo Médio de Aluguel vs Clima:**
    * **Objetivo:** Calcular o tempo médio de aluguel de filmes por cidade e analisar visualmente sua correlação com a temperatura atual dessas cidades.
    * **Fontes:** Pagila (tabelas `rental`, `customer`, `address`, `city`), WeatherAPI.
    * **Lógica:** Consulta SQL para calcular o tempo médio de aluguel em segundos por cidade, considerando apenas cidades com mais de 20 aluguéis. Converter para dias. Obter a temperatura atual para essas cidades.
    * **Saída:** Tabela com tempo médio de aluguel e temperatura, um scatterplot (`seaborn`) mostrando a relação e o coeficiente de correlação de Pearson.

* **Exercício 8 – Perfil de Clima por Cliente:**
    * **Objetivo:** Para uma amostra de clientes, criar um perfil detalhado (cidade, temperatura, AQI, total de aluguéis, gasto total). Agrupar esses perfis por uma faixa etária simulada para identificar possíveis padrões de consumo em relação a fatores ambientais.
    * **Fontes:** Pagila, WeatherAPI, AirVisual API.
    * **Lógica:** Consulta SQL para dados base do cliente. Para uma amostra de cidades, buscar temperatura e AQI. Fazer o merge. Simular faixas etárias. Agrupar e analisar médias de gasto.
    * **Saída:** Tabelas mostrando o perfil de cliente (amostra), gasto total médio por faixa etária simulada, e por faixa etária e qualidade do ar.

* **Exercício 9 – Exportação Inteligente:**
    * **Objetivo:** Gerar um relatório Excel com múltiplas abas, contendo clientes que atendem a critérios ambientais e de consumo específicos.
    * **Fontes:** Dados processados do Exercício 8.
    * **Lógica:** Filtrar o DataFrame de perfis de clientes com base nos critérios (temperatura < 15°C, AQI > 100, gasto > média). Preparar DataFrames para abas ("Clientes\_Criticos", "Condicoes\_Temperatura", "Alertas\_Ambientais\_Consumo"). Escrever para Excel.
    * **Saída:** Mensagem sobre a geração do relatório. (Na execução de exemplo, nenhum cliente da amostra satisfez os filtros).

* **Exercício 10 – API Cache Inteligente (Desafio):**
    * **Objetivo:** Demonstrar a funcionalidade do sistema de cache implementado para as chamadas às APIs.
    * **Lógica:** As funções de cache e as funções de API modificadas são definidas anteriormente. Esta célula executa chamadas de teste, mostrando "CACHE HIT" ou "API CALL".
    * **Saída:** Logs de teste do cache.

**Considerações Finais e Fechamento:**
* O notebook conclui com fechamento opcional da conexão com o banco.
* **Avisos:** `UserWarning` do Pandas (sugestão de SQLAlchemy) e `SettingWithCopyWarning`s (tratados com `.copy()` e `.loc`).
* **Eficiência:** Uso de amostras (`.head(N)`, `.sample(N)`) para agilidade e para evitar limites de API.

**Aprendizados Chave Esperados:**
Ao completar este notebook, o usuário deve ganhar experiência prática em:
* Conectar Python a PostgreSQL e executar SQL.
* Consumir dados de APIs RESTful.
* Limpar, transformar, e combinar dados de múltiplas fontes (Pandas).
* Gerenciar chaves de API.
* Implementar cache para otimizar chamadas de API.
* Realizar análises exploratórias e gerar visualizações.
* Exportar resultados para Excel.
* Lidar com desafios práticos de integração de dados.