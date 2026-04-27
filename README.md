Projeto Final Bootcamp Data Science & AI - Le Wagon

Stock vs. Behavior

Atualmente, vivemos na era digital, em um mundo interconectado onde informações e tecnologias estão acessíveis a todo momento, literalmente na palma da nossa mão.

Nossas decisões estão a apenas um clique de distância. Gostos pessoais, hábitos de consumo, comportamentos, viagens, tudo sofre a influência de notícias, opiniões de terceiros, influenciadores, amigos e familiares às quais somos submetidos diariamente.

E no mercado financeiro, seria diferente? Como essa superexposição a diversos tipos de conteúdo pode influenciar o comportamento das ações na bolsa de valores?

Nosso projeto busca demonstrar como as principais notícias podem impactar o preço das ações, considerando que muitos investidores baseiam suas operações nos acontecimentos do momento.

Projeto elaborado por: Evandro Herrera, Guilherme Dutra, Letícia Mesquita e Nathália Montandon

## Executando o aplicativo

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Depois de iniciar, acesse:

- Localmente: `http://localhost:10000`
- Alternativa local: `http://127.0.0.1:10000`

Se o terminal mostrar `http://0.0.0.0:10000`, não use esse endereço no navegador.
`0.0.0.0` indica apenas que o servidor está escutando em todas as interfaces.

O aplicativo procura primeiro pelos artefatos completos gerados pelos notebooks:

- `data/processed/aapl_data.csv`
- `models/aapl_rnn_model.keras`
- `models/aapl_target_scaler.pkl`
- `models/aapl_feature_scaler.pkl`

Como esses diretórios são ignorados pelo Git, uma instalação limpa usa `sample_data/aapl_data.csv`
e exibe uma previsão de referência baseada na última cotação disponível. Para usar o modelo
treinado, gere ou copie os artefatos acima para os caminhos esperados.
