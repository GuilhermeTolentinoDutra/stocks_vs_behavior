import streamlit as st
import pandas as pd

from utils.app_functions import (
    compute_predicted_date,
    get_prediction_mode_message,
    load_price_data,
    predict,
)

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

data, data_message = load_price_data()
data = data[data["Date"] >= pd.to_datetime("2009-08-07").date()].copy()

if data_message:
    st.warning(data_message)

prediction_mode_message = get_prediction_mode_message()
if prediction_mode_message:
    st.info(prediction_mode_message)

stock_price_df = data[["Date", "AAPL"]].rename({"AAPL": "Close"}, axis=1)
stock_price_df = stock_price_df.sort_values("Date").drop_duplicates("Date", keep="last")

available_dates = stock_price_df["Date"].tolist()
if len(available_dates) < 2:
    st.error("The app needs at least two trading days to calculate a forecast.")
    st.stop()

min_index = min(30, len(available_dates) - 2)
min_date = available_dates[min_index]
max_date = available_dates[-2]

default_index = min(max(min_index, len(available_dates) // 2), len(available_dates) - 2)
default_date = available_dates[default_index]
min_date_str = min_date.strftime(format="%d/%m/%Y")
max_date_str = max_date.strftime(format="%d/%m/%Y")

# Input da data cuja previsão será realizada
selected_date = st.sidebar.date_input(
    f"Selecione a data ({min_date_str} a {max_date_str}):",
    value=default_date,
    min_value=min_date,
    max_value=max_date,
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
    st.dataframe(filtered_data, hide_index=True, use_container_width=True, height=250)

with col2:
    predicted_date = compute_predicted_date(available_dates, selected_date)
    predicted_date_str = predicted_date.strftime(format="%d de %b de %Y")

    st.write(f"## {predicted_date_str}")

    last_price = float(filtered_data.iloc[0]["Close"])

    col1_predicted, col2_predicted = st.columns([1, 1], gap="medium")
    with col1_predicted:
        predicted_price = predict(data, selected_date)
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
