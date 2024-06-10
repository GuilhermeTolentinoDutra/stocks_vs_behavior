
import streamlit as st
import time
import pandas as pd

st.set_page_config(page_title='Stock vs. Behavior',
                   page_icon='/root/code/NathaliaMontandon/stocks_vs_behavior/pages/icone.jpg',
                   layout="wide")



st.header('Stock vs. Behavior')

data = pd.read_csv('/root/code/NathaliaMontandon/stocks_vs_behavior/data/processed/stock_market_dataset.csv')
data['Date'] = pd.to_datetime(data['Date']).dt.date
data = data.drop(columns=['Unnamed: 0'])


#### Add a selectbox to the sidebar:
####Item funcionando corretamente
value = st.sidebar.selectbox(
    'Selecione o seu ativo',  data.Stock.unique()
    # ('Amazon', 'Apple', 'Google', 'Microsoft', 'Nvidia')
)


date_options = data['Date'].unique().tolist()
date = st.sidebar.slider("Selecione o período:", 2008,2016, (2008,2016))
date_options = sorted(data['Date'].unique())

# Filtrar DataFrame com base na seleção
filtered_data = data[(data['Stock'] == value) & (data['Date'] >= date_options[0]) & (data['Date'] <= date_options[1])]

# st.subheader('DataFrame Filtrado')

##### fim




col1, col2, col3= st.columns([1,2,1], gap='medium')
with col1:
    st.write("## Cotação histórica:")
    col1=st.dataframe(filtered_data)
filtered_data.set_index('Date', inplace=True)

with col2:
   st.write("Gráfico histórico")

   # You can call any Streamlit command, including custom components:
   st.line_chart(filtered_data, y=['Close'])

with col3:
    st.write(pd.DataFrame({
        ' Stock': ['D+1','D+2','D+3','D+4'],
        'Close': [10, 20, 30, 40]
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
