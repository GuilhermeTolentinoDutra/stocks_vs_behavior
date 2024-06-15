# Importação de bibliotecas
import datetime
import streamlit as st
import pandas as pd


st.set_page_config('Stock vs. Behavior - Quanto irá valer?',
                   page_icon='/root/code/NathaliaMontandon/stocks_vs_behavior/pages/icone.jpg',
                   layout="wide")

text = 'Stock vs. Behavior - Quanto irá valer?'


# Configurações da página
st.markdown(f"""
    <style>
    .centered-text {{
        color: #0000ff;
        text-align: center;
        font-size: 40px;
    }}
    </style>
    <div class="centered-text">
        {text}
    </div>
    """, unsafe_allow_html=True)


# Carregamento e tratamento dos dados
data = pd.read_csv('/root/code/NathaliaMontandon/stocks_vs_behavior/data/processed/stock_market_dataset.csv')
data['Date'] = pd.to_datetime(data['Date']).dt.date
data = data.drop(columns=['Unnamed: 0'])

st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        font-size: 20px; /* Altere o valor para o tamanho desejado */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Selectbox para selecionar a ação desejada
value = st.sidebar.selectbox(
    'Selecione o seu ativo',  data.Stock.unique()
    #  ('Amazon', 'Apple', 'Google', 'Microsoft', 'Nvidia')
)

# date = st.sidebar.date_input("Selecione a data:", min_value=2008, max_value=2016, key=None, help=None, on_change=None, args=None, kwargs=None, *, format="YYYY/MM/DD", disabled=False, label_visibility="visible")
# d = st.date_input("When's your birthday", datetime.date(2019, 7, 6))
# st.write("Your birthday is:", d)

# Input da data cuja previsão será realizada
d = st.sidebar.date_input("Selecione a data (06/09/2008 a 30/07/2016):", value=None, min_value=datetime.date(2008,6,9), max_value=datetime.date(2016,7,30))
# st.sidebar.write("Your birthday is:", d)

# Retorno dos dados filtrados
filtered_data = data[data['Stock'] == value]





# Seleção de dias para predição
# a = st.sidebar.radio('Selecione o período da predição (em dias):', ['1','3','7'])

# Separação da tela principal em três colunas, a primeira com as cotações históricas, a segunda com o gráfico histórico da ação selecionada e o terceiro com o valor predito
col1, col2, col3= st.columns([1,2,1], gap='medium')
with col1:
    st.write("## Cotação histórica:")
    col1=st.dataframe(filtered_data)
    # filtered_data.set_index('Date', inplace=True)

with col2:
    st.write("## Gráfico histórico")
    st.line_chart(filtered_data, y=['Close'])

with col3:
    st.write('## Cotação Prevista')
    st.write(pd.DataFrame({
        ' Stock': [d],
        'Predicted price': [10]
    }))



# date_options = data['Date'].unique().tolist()
# date = st.sidebar.slider("Selecione o período:", 2008,2016, (2008,2016))
# date_options = sorted(data['Date'].unique())

# # Criar um slider no Streamlit para selecionar o período
# start_year, end_year = st.sidebar.slider(
#     "Selecione o período:",
#     min_value=date_options[0],
#     max_value=date_options[-1],
#     )




st.write('---')
st.markdown('<div style="text-align: center">Projeto de conclusão do bootcamp Data Science and AI - Batch 1532. Junho 2024</div>', unsafe_allow_html=True)
