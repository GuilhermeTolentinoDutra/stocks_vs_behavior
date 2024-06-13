import streamlit as st

st.set_page_config(page_title='Grupo',
                   page_icon='/root/code/NathaliaMontandon/stocks_vs_behavior/pages/icone.jpg',
                   layout="wide")

tab1, tab2, tab3, tab4 = st.tabs(["Evandro Herrera", "Guilherme Dutra", "Letícia Mesquita", " Nathália Montandon"])

with tab1:
   st.header("Evandro Herrera")
   st.image("/root/code/NathaliaMontandon/stocks_vs_behavior/app_data/evandro.jpg", width=200)
   '''With over 23 years of experience in Information Technology, I have specialized in the financial sector, where I have developed a strong expertise in team leadership, system development, and project management. My background includes extensive experience in financial analysis, cash flow management, and budget development, as well as a comprehensive understanding of the entire process chain, from front office operations to accounting and P&L calculations. I possess a deep knowledge of various financial products, including fixed income, derivatives, loans, foreign exchange, and offshore investments. Proficient in all stages of project development, I focus on requirements analysis, delivery monitoring, documentation, user support, and process optimization.'''

with tab2:
   st.header("Guilherme Dutra")
   st.image('/root/code/NathaliaMontandon/stocks_vs_behavior/app_data/guilherme.jpg')
   '''Sou advogado, possuo mais de 14 anos de experiência, notadamente em direito penal e, posteriormente, em contratos. Hoje, busco na programação uma oportunidade de crescimento e nova carreira.
   Sempre gostei de tecnologia e agora quero me dedicar a essa área e aproveitar as oportunidades que ela proporciona'''


with tab3:
   st.header("Letícia Mesquita")
   st.image("/root/code/NathaliaMontandon/stocks_vs_behavior/app_data/leticia.jpg", width=200)
   '''My name is Letícia Mesquita, I am 29 years old and I'm from Rio de Janeiro.
   My academic background revolves around Chemistry, as I hold degrees both as a technician and a licentiate.
   I have experience in research, teaching, and the pharmaceutical industry. I worked in the production sector of the national Covid vaccine at Fiocruz during the pandemic and, currently, I am a quality control analyst at Merck.
   I am very curious, love learning new things, and see a career in data science as an opportunity for a better quality of life, work, and connection with the present/future.'''

with tab4:
    st.header("Nathália Montandon")
    st.image('/root/code/NathaliaMontandon/stocks_vs_behavior/app_data/nathalia.jpg', width=200)

    '''Durante a faculdade tive uma matéria de Excel avançado, a qual me interessou tanto que no meu tempo livre passei a estudar mais sobre a ferramenta e a desenvolver alguns projetos. Diante disso, me sugeriram aprender alguma linguagem de programação. Sendo assim, comecei a estudar Python pelo Youtube, pouco tempo depois comprei cursos para me aprofundar no assunto e comecei a desenvolver projetos utilizando essa linguagem. Depois de um pouco mais de 1 ano estudando comecei a buscar uma oportunidade para atuar com dados. Atualmente, estou há dois anos trabalhando nessa área
    Meu interesse em fazer um bootcamp deve-se a três pontos principais:
    • Orientação mais próxima
    o Acredito que ter um acompanhamento mais próximo e profissional do meu desenvolvimento técnico pode ser muito benéfico para impulsionar meus conhecimentos
    • Back to the basics
    o Como sempre estudei por conta própria, acho que alguns conceitos básicos não foram tão bem desenvolvidos e aprimorá-los é essencial para ter uma base sólida.
    • Novos conhecimentos
    o Além disso, quero aprofundar meu repertório na área de dados, especialmente ciência de dados, para alavancar minha carreira e ser capaz de gerar cada vez mais valor.'''


st.write('---')
st.markdown('<div style="text-align: center;">Projeto de conclusão do bootcamp Data Science and AI - Batch 1532. Junho 2024</div>', unsafe_allow_html=True)
