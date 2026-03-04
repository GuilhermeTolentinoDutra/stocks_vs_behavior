import streamlit as st
import os

st.set_page_config(page_title='O Projeto',
                   page_icon=os.path.join(os.path.dirname(__file__), 'icone.jpg'),
                   layout="wide")

st.markdown(
    """
    <h1 style='text-align: center; color: #4b0081;'>
        Ações vs. Comportamentos<br>
        <small>COMPORTAMENTOS INFLUENCIAM</small><br>
        <small>... o comportamento dos consumidores</small>
    </h1>
    """,
    unsafe_allow_html=True)

text_1 = '''
•	Notícias sobre a marca;\n
•	Experiência própria e de conhecidos;\n
•	Avalições de outros consumidores;\n
•	Comportamento alheio.

NO MERCADO FINANCEIRO
... não seria diferente

Qual o impacto dos comportamentos na cotação das ações?

DADOS:

### HUGE STOCK MARKET DATA SET \n
Cotação histórica das ações negociadas nas bolsas dos EUA \n
https://www.canva.com/link?target=https%3A%2F%2Fwww.kaggle.com%2Fdatasets%2Fborismarjanovic%2Fprice-volume-data-for-all-us-stocks-etfs&design=DAGEvI8B6kI&accessRole=viewer&linkSource=document'''
st.markdown(f"""
    <div style="text-align:center; color: #4b0081; font-size: 18px;">
        {text_1}
    </div>
    """, unsafe_allow_html=True)

if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app_data', 'hsmdataset.jpg')):
    image_1 = st.image(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app_data', 'hsmdataset.jpg'))

text_2 = ''' ### DAILY NEWS FOR STOCK MARKET PREDICTION \n
Notícias mais votadas no Reddit WorldNews Channel diariamente \n
https://www.canva.com/link?target=https%3A%2F%2Fwww.kaggle.com%2Fdatasets%2Faaron7sun%2Fstocknews%3Fselect%3DCombined_News_DJIA.csv&design=DAGEvI8B6kI&accessRole=viewer&linkSource=document'''
st.markdown(f"""
    <div style="text-align:center; color: #4b0081; font-size: 18px;">
        {text_2}
    </div>
    """, unsafe_allow_html=True)

if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app_data', 'redditnews.jpg')):
    image_2 = st.image(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app_data', 'redditnews.jpg'))

text_3 = '''TECNOLOGIAS E FERRAMENTAS
... que poderão ser utilizadas \n
O QUÊ:
Prever a cotação da ação X em uma data futura, considerando múltiplas variáveis, e baseando-se em dados passados desse ativo, assim como no comportamento da população. \n
COMO:
Recurrent Neural Networks (RNN) \n
Transformers'''

st.markdown(f"""
    <div style="text-align:center; color: #4b0081; font-size: 18px;">
        {text_3}
    </div>
    """, unsafe_allow_html=True)
st.markdown(
    """
    <h1 style='text-align: center; color: #4b0081;'>
        VAMOS PREVER O MERCADO?
    </h1>
    """,
    unsafe_allow_html=True
)
st.write('---')
st.markdown('<div style="text-align: center;">Projeto de conclusão do bootcamp Data Science and AI - Batch 1532. Junho 2024</div>', unsafe_allow_html=True)
