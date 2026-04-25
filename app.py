# Importação de bibliotecas
import streamlit as st
import pandas as pd
import os

from utils.app_functions import (
    ModelArtifactsError,
    compute_predicted_date,
    fallback_predict,
    predict,
)

path_pages = os.path.join(os.path.abspath(""), "pages")
path_processed_data = os.path.join(os.path.abspath(""), "data", "processed")

st.set_page_config(
    "Stock vs. Behavior - Quanto irá valer?",
    page_icon="📈",
    layout="wide",
)

text = "Stock vs. Behavior?"
subtitle = "Quanto a AAPL irá valer de acordo com as notícias?"

# Configurações da página  #0000ff
st.markdown(
    f"""
        <div style="color: #5f52f2; text-align: center; font-size: 40px; font-weight: bold;">
            {text}
        </div>
        <div style="text-align: center; font-size: 20px;">
            {subtitle}
        </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# Carregamento e tratamento dos dados
data = pd.read_csv(os.path.join(path_processed_data, "aapl_data.csv"))

data = data[data["Date"] >= "2009-08-07"]

data["Date"] = pd.to_datetime(data["Date"]).dt.date

stock_price_df = data[["Date", "AAPL"]].copy()
stock_price_df.rename({"AAPL": "Close"}, axis=1, inplace=True)
stock_price_df = stock_price_df.sort_values("Date").drop_duplicates("Date", keep="last")

min_date = stock_price_df["Date"].min() + pd.DateOffset(days=30)
max_date = stock_price_df["Date"].max()
available_dates = stock_price_df["Date"].sort_values().drop_duplicates()
max_selectable_date = available_dates.iloc[-2] if len(available_dates) > 1 else max_date

min_date_str = min_date.strftime(format="%d/%m/%Y")
max_date_str = pd.to_datetime(max_selectable_date).strftime(format="%d/%m/%Y")

# Input da data cuja previsão será realizada
selected_date = st.sidebar.date_input(
    f"Selecione a data ({min_date_str} a {max_date_str}):",
    value=min_date,
    min_value=min_date,
    max_value=max_selectable_date,
)

selected_date = pd.to_datetime(selected_date).date()

# Retorno dos dados filtrados
filtered_data = stock_price_df[(stock_price_df["Date"] <= selected_date)].sort_values(
    "Date", ascending=False
)

# Separação da tela principal em três colunas, a primeira com as cotações
# históricas, a segunda com o gráfico histórico da ação selecionada e o
# terceiro com o valor predito
col1, col2 = st.columns([1, 1], gap="large")  # , col3
with col1:
    st.write("## Cotação Histórica")
    st.dataframe(filtered_data, hide_index=True, width="stretch", height=250)

with col2:
    predicted_date = compute_predicted_date(
        min_date,
        max_date,
        selected_date,
        available_dates=available_dates,
    )

    if predicted_date is None or filtered_data.empty:
        st.warning("Não há dados futuros disponíveis para a data selecionada.")
        st.stop()

    predicted_date_str = predicted_date.strftime(format="%d de %b de %Y")

    st.write(f"## {predicted_date_str}")
    last_price = float(filtered_data.iloc[0]["Close"])

    col1_predicted, col2_predicted = st.columns([1, 1], gap="medium")
    with col1_predicted:
        try:
            predicted_price = predict(data, selected_date)
        except ModelArtifactsError as error:
            predicted_price = fallback_predict(data, selected_date)
            st.warning(
                f"{error} Exibindo a previsão de fallback baseada nos dados."
            )

        predicted_delta = ((predicted_price - last_price) / last_price) * 100

        st.metric(
            label="Cotação Prevista",
            value=f"US$ {predicted_price:.2f}",
            delta=f"{predicted_delta:.4f}%",
        )

    with col2_predicted:
        real_price = stock_price_df[stock_price_df["Date"] == predicted_date].iloc[0][
            "Close"
        ]
        real_delta = ((real_price - last_price) / last_price) * 100

        st.metric(
            label="Cotação Real",
            value=f"US$ {real_price:.2f}",
            delta=f"{real_delta:.4f}%",
        )

    col1_dif, col2_dif = st.columns(2, gap="medium")
    with col1_dif:
        dif_price = predicted_price - real_price
        dif_delta = predicted_delta - real_delta

        st.metric(
            label="Diferença",
            value=f"US$ {dif_price:.2f}",
            delta=f"{dif_delta:.4f} p.p.",
        )

st.write("## Gráfico da Cotação Histórica")
st.line_chart(filtered_data, x="Date", y=["Close"], color="#5f52f2")

st.write("---")
st.markdown(
    '<div style="text-align: center">Projeto de conclusão do bootcamp Data Science and AI - Batch 1532. Junho 2024</div>',
    unsafe_allow_html=True,
)
