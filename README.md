Projeto Final Bootcamp Data Science & AI - Le Wagon

Stock vs. Behavior

Atualmente, vivemos na era digital, em um mundo interconectado onde informações e tecnologias estão acessíveis a todo momento, literalmente na palma da nossa mão.

Nossas decisões estão a apenas um clique de distância. Gostos pessoais, hábitos de consumo, comportamentos, viagens, tudo sofre a influência de notícias, opiniões de terceiros, influenciadores, amigos e familiares às quais somos submetidos diariamente.

E no mercado financeiro, seria diferente? Como essa superexposição a diversos tipos de conteúdo pode influenciar o comportamento das ações na bolsa de valores? 

Nosso projeto busca demonstrar como as principais notícias podem impactar o preço das ações, considerando que muitos investidores baseiam suas operações nos acontecimentos do momento.

Projeto elaborado por: Evandro Herrera, Guilherme Dutra, Letícia Mesquita e Nathália Montandon

## Como executar

Este repositório contem uma aplicacao Streamlit.

1. Crie um ambiente virtual Python 3.11+.
2. Instale as dependencias:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

3. Inicie a aplicacao:

   ```bash
   python3 -m streamlit run app.py
   ```

### Observacoes sobre os dados

- Se `data/processed/aapl_data.csv` estiver presente, a aplicacao usa o dataset processado do projeto.
- Se os arquivos em `models/` estiverem presentes, a previsao usa o modelo treinado.
- Em um checkout limpo, esses artefatos normalmente nao existem porque estao no `.gitignore`. Nesse caso a aplicacao agora inicia em modo demonstracao, com um dataset embutido e uma previsao heuristica para que a interface continue funcionando.
