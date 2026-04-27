import pickle
import numpy as np
import os
import pandas as pd
import streamlit as st
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path_models = os.path.join(PROJECT_ROOT, "models")


def get_model_artifact_paths():
    return (
        os.path.join(path_models, "aapl_rnn_model.keras"),
        os.path.join(path_models, "aapl_target_scaler.pkl"),
        os.path.join(path_models, "aapl_feature_scaler.pkl"),
    )


def _missing_model_message():
    return (
        "Modo demonstração: os arquivos do modelo treinado não foram encontrados em "
        "`models/`. A cotação exibida é uma referência baseada na última cotação "
        "disponível, não uma previsão do modelo."
    )


@st.cache_resource
def load_model_and_scalers():
    model_path, target_scaler_path, feature_scaler_path = get_model_artifact_paths()

    if not all(
        os.path.isfile(path) and os.path.getsize(path) > 0
        for path in (model_path, target_scaler_path, feature_scaler_path)
    ):
        return None, None, None, _missing_model_message()

    try:
        import tensorflow as tf
    except ModuleNotFoundError:
        return (
            None,
            None,
            None,
            "Modo demonstração: os arquivos do modelo foram encontrados, mas o "
            "TensorFlow não está instalado. Instale `tensorflow` para habilitar a "
            "previsão do modelo.",
        )

    try:
        model = tf.keras.models.load_model(
            model_path,
        )

        with open(target_scaler_path, "rb") as f:
            target_scaler = pickle.load(f)

        with open(feature_scaler_path, "rb") as f:
            feature_scaler = pickle.load(f)
    except Exception as exc:
        return (
            None,
            None,
            None,
            "Modo demonstração: os arquivos em `models/` existem, mas não puderam "
            f"ser carregados ({type(exc).__name__}: {exc}). Confira se o arquivo "
            "`.keras` e os scalers `.pkl` foram copiados corretamente.",
        )

    return model, target_scaler, feature_scaler, None


def get_model_status_message():
    _, _, _, status_message = load_model_and_scalers()
    return status_message


def predict(data, selected_date):
    model, target_scaler, feature_scaler, _ = load_model_and_scalers()
    data_predict = data[data["Date"] <= selected_date].copy()

    if model is None:
        return float(data_predict.iloc[-1]["AAPL"])

    data_predict["AAPL_target"] = target_scaler.transform(data_predict[["AAPL_target"]])

    data_predict["AAPL"] = feature_scaler.transform(data_predict[["AAPL"]])

    features = ["AAPL", "negative", "neutral", "positive"]

    X = []
    length = 30
    for i in range(length, data_predict.shape[0]):
        X.append(data_predict[features].iloc[i - length : i])

    X = np.array(X)

    y_pred = model.predict(X)

    prediction = target_scaler.inverse_transform(y_pred)

    return prediction[-1, -1]


def compute_predicted_date(min_date, max_date, selected_date):
    calendar = pd.DataFrame(
        pd.date_range(
            start=min_date,
            end=max_date,
            freq=CustomBusinessDay(calendar=USFederalHolidayCalendar()),
        ),
        columns=["Date"],
    )

    calendar["Date"] = pd.to_datetime(calendar["Date"]).dt.date

    predicted_date = pd.to_datetime(
        calendar[calendar["Date"] > selected_date].iloc[0]["Date"]
    ).date()

    return predicted_date
