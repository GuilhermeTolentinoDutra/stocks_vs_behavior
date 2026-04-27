# Stock vs. Behavior

Projeto final do Bootcamp Data Science & AI da Le Wagon - Batch 1532.

**Autores:** Evandro Herrera, Guilherme Dutra, Letícia Mesquita e Nathália Montandon.

## Sobre o projeto

Vivemos em um ambiente digital no qual notícias, opiniões, avaliações e comportamentos
coletivos influenciam decisões de consumo e investimento. No mercado financeiro, esse
fluxo de informação pode impactar a percepção sobre empresas e, consequentemente, o
comportamento de suas ações.

O **Stock vs. Behavior** investiga essa relação usando dados históricos de ações e sinais
de sentimento extraídos de notícias. A versão atual do aplicativo foca na ação da Apple
(**AAPL**) e permite selecionar uma data para comparar:

- a cotação histórica até a data escolhida;
- a cotação real do próximo dia útil disponível;
- a previsão do modelo treinado, quando os artefatos do modelo estão disponíveis;
- ou uma cotação de referência em modo demonstração, quando o modelo não está disponível.

## Objetivo

Demonstrar um fluxo de ciência de dados que combina:

1. dados financeiros históricos;
2. notícias/textos relacionados ao mercado;
3. análise de sentimento;
4. modelagem temporal com redes neurais recorrentes;
5. uma interface Streamlit para consulta e apresentação dos resultados.

## Fontes de dados

O projeto foi construído a partir de bases públicas usadas durante o desenvolvimento nos
notebooks:

- **Huge Stock Market Dataset**: cotações históricas de ações e ETFs negociados nos EUA.
- **Daily News for Stock Market Prediction**: notícias diárias do canal Reddit WorldNews.
- Dados/notícias financeiros usados para classificação de sentimento em notebooks de
  modelagem de linguagem financeira.

> Observação: os diretórios `data/` e `models/` estão ignorados pelo Git porque podem conter
> arquivos grandes ou gerados localmente. Por isso, o repositório inclui uma amostra em
> `sample_data/aapl_data.csv` para que o app rode mesmo em uma instalação limpa.

## Etapas do projeto

### 1. Análise exploratória

Notebook principal:

- `notebooks/0_exploratory_analysis.ipynb`

Nesta etapa foram exploradas referências como S&P 500, NASDAQ Screener, dados de mercado
e notícias diárias. O objetivo foi entender as bases disponíveis, formatos, períodos e
possíveis relações entre eventos/notícias e comportamento de preços.

### 2. ETL dos dados financeiros

Notebooks principais:

- `notebooks/1_etl_huge_stock_market.ipynb`
- `notebooks/1_etl_stock_prices.ipynb`

Nesta etapa o projeto extrai, transforma e organiza dados de cotações. O foco da aplicação
final é a ação **AAPL**, mas os notebooks também exploram bases mais amplas de mercado.

Principais atividades:

- leitura de arquivos brutos de cotações;
- seleção e padronização de colunas relevantes;
- preparação da série temporal por data;
- integração inicial com dados de notícias.

### 3. Classificação de sentimento das notícias

Notebooks principais:

- `notebooks/2_model_financial_news.ipynb`
- `notebooks/2_model_reddit.ipynb`

Nesta etapa foram usados modelos de linguagem voltados a sentimento financeiro, com base
em RoBERTa fine-tuned para notícias financeiras. As notícias são classificadas em classes
como:

- `negative`;
- `neutral`;
- `positive`.

Esses sinais são usados posteriormente como variáveis explicativas para o modelo temporal.

### 4. Transformação e agregação de sentimento por data

Notebooks principais:

- `notebooks/3_transform_analystis_rating.ipynb`
- `notebooks/3_transform_reddit_news_sentiment.ipynb`

Depois da classificação, os sentimentos são agregados por data. Essa etapa transforma um
conjunto de notícias em features numéricas diárias, por exemplo:

- percentual de notícias negativas por dia;
- percentual de notícias neutras por dia;
- percentual de notícias positivas por dia;
- scores médios de sentimento por data.

O resultado esperado para a aplicação é uma base consolidada com colunas como:

```text
Date,AAPL,AAPL_target,negative,neutral,positive
```

### 5. Modelagem temporal com RNN

Notebooks principais:

- `notebooks/4_RNN_model_GRU.ipynb`
- `notebooks/4_RNN_model_LSTM.ipynb`
- `notebooks/4_RNN_model_GRU_analystis_rating_AAPL.ipynb`
- `notebooks/4_RNN_model_GRU_analystis_rating_dropout_AAPL.ipynb`
- `notebooks/4_RNN_model_GRU_analystis_rating_grid_search_AAPL.ipynb`

Nesta etapa foram treinadas redes neurais recorrentes para previsão da cotação futura.
Foram testadas arquiteturas como:

- GRU;
- LSTM;
- regularização;
- dropout;
- busca de hiperparâmetros.

A aplicação Streamlit usa uma janela temporal de **30 observações anteriores** e as features:

```python
["AAPL", "negative", "neutral", "positive"]
```

Quando o modelo treinado está disponível, o app carrega:

```text
models/aapl_rnn_model.keras
models/aapl_target_scaler.pkl
models/aapl_feature_scaler.pkl
```

### 6. Validação

Notebook principal:

- `notebooks/5_model_validation.ipynb`

Essa etapa concentra a avaliação dos resultados e comparação entre cotações previstas e
reais. No app, essa comparação aparece nos indicadores:

- `Cotação Prevista` ou `Cotação de Referência`;
- `Cotação Real`;
- `Diferença`.

## Aplicativo Streamlit

Arquivo principal:

- `app.py`

O app permite selecionar uma data na barra lateral e exibe:

1. tabela com a cotação histórica até a data selecionada;
2. previsão/referência para o próximo dia útil;
3. cotação real do próximo dia útil;
4. diferença entre previsão/referência e valor real;
5. gráfico da série histórica.

Páginas adicionais:

- `pages/Projeto.py`: apresentação conceitual do projeto;
- `pages/Grupo.py`: apresentação do grupo.

## Estrutura do repositório

```text
.
├── app.py
├── pages/
│   ├── Grupo.py
│   └── Projeto.py
├── utils/
│   └── app_functions.py
├── notebooks/
│   ├── 0_exploratory_analysis.ipynb
│   ├── 1_etl_huge_stock_market.ipynb
│   ├── 1_etl_stock_prices.ipynb
│   ├── 2_model_financial_news.ipynb
│   ├── 2_model_reddit.ipynb
│   ├── 3_transform_analystis_rating.ipynb
│   ├── 3_transform_reddit_news_sentiment.ipynb
│   ├── 4_RNN_model_*.ipynb
│   └── 5_model_validation.ipynb
├── sample_data/
│   └── aapl_data.csv
├── requirements.txt
└── README.md
```

Diretórios esperados, mas não versionados:

```text
data/
models/
```

## Como executar o aplicativo

### 1. Criar e ativar ambiente virtual

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Rodar o Streamlit

```bash
streamlit run app.py
```

Depois de iniciar, acesse:

- `http://localhost:10000`
- ou `http://127.0.0.1:10000`

Se o terminal mostrar `http://0.0.0.0:10000`, não use esse endereço no navegador.
`0.0.0.0` indica apenas que o servidor está escutando em todas as interfaces.

## Modo demonstração

O repositório roda mesmo sem os arquivos reais de dados e modelo. Nesse caso:

- o app usa `sample_data/aapl_data.csv` se `data/processed/aapl_data.csv` não existir;
- o app mostra `Cotação de Referência` se o modelo treinado não estiver disponível;
- a referência é a última cotação disponível até a data selecionada;
- isso mantém a interface funcional, mas não representa uma previsão real do modelo.

Se você não tiver os artefatos reais do modelo, pode remover uma pasta `models/` local
incompleta para evitar confusão:

```bash
rm -rf models
```

## Como usar a previsão real do modelo

Para habilitar `Cotação Prevista`, copie ou gere os seguintes arquivos:

```text
data/processed/aapl_data.csv
models/aapl_rnn_model.keras
models/aapl_target_scaler.pkl
models/aapl_feature_scaler.pkl
```

Também instale TensorFlow no ambiente:

```bash
pip install tensorflow
```

Em seguida, reinicie o app:

```bash
streamlit run app.py
```

Se qualquer arquivo em `models/` estiver ausente, vazio, incompatível ou inválido, o app
continua em modo demonstração em vez de interromper a execução.

## Dependências principais

As dependências mínimas para rodar o app em modo demonstração estão em `requirements.txt`:

- `numpy`
- `pandas`
- `scikit-learn`
- `fastapi`
- `streamlit`

Para carregar o modelo real, instale também:

- `tensorflow`

## Limitações conhecidas

- A versão publicada no Git não inclui as bases completas nem os artefatos do modelo.
- Sem `models/`, os valores exibidos são referências, não previsões reais.
- O modelo foi desenvolvido para AAPL; generalizar para outros ativos exige novo preparo de
  dados, features e treinamento.
- Resultados de modelos financeiros não devem ser interpretados como recomendação de
  investimento.

## Aviso

Este projeto tem finalidade educacional e demonstrativa. Ele não constitui recomendação de
compra, venda ou manutenção de ativos financeiros.
