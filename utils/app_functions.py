import tensorflow as tf
import pickle
import numpy as np
import os
import pandas as pd
import streamlit as st
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

path_models = os.path.join(os.path.abspath(""), "models")


class _GRULegacyCompat(tf.keras.layers.GRU):
    """Older Keras/TF checkpoints may serialize GRU with `time_major`; strip it for Keras 3."""

    @classmethod
    def from_config(cls, config):
        cfg = dict(config)
        cfg.pop("time_major", None)
        return super().from_config(cfg)


@st.cache_resource
def load_model_and_scalers():
    # Load model (HDF5 checkpoint saved as .h5; legacy name was .keras but was not zip format)
    model = tf.keras.models.load_model(
        os.path.join(path_models, "aapl_rnn_model.h5"),
        custom_objects={"GRU": _GRULegacyCompat},
        compile=False,
    )

    # Load scaler applied to target column
    with open(os.path.join(path_models, "aapl_target_scaler.pkl"), "rb") as f:
        target_scaler = pickle.load(f)

    with open(os.path.join(path_models, "aapl_feature_scaler.pkl"), "rb") as f:
        feature_scaler = pickle.load(f)

    return model, target_scaler, feature_scaler


def predict(data, selected_date):
    model, target_scaler, feature_scaler = load_model_and_scalers()

    # selected_date = selected_date + " 23:59:59"
    data_predict = data[data["Date"] <= selected_date]
    data_predict["AAPL_target"] = target_scaler.transform(data_predict[["AAPL_target"]])

    data_predict["AAPL"] = feature_scaler.transform(data_predict[["AAPL"]])

    features = ["AAPL", "negative", "neutral", "positive"]

    X = []
    length = 30
    for i in range(length, data_predict.shape[0]):
        X.append(data_predict[features].iloc[i - length : i])

    X = np.array(X)

    y_pred = model.predict(X)

    print(y_pred)

    prediction = target_scaler.inverse_transform(y_pred)

    print(prediction)

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
