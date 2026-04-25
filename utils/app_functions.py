import os
import pickle
import shutil
import tempfile

os.environ.setdefault("TF_USE_LEGACY_KERAS", "1")

import numpy as np
import pandas as pd
import streamlit as st
import tensorflow as tf
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

path_models = os.path.join(os.path.abspath(""), "models")


def _load_legacy_compatible_model(model_path):
    try:
        return tf.keras.models.load_model(model_path)
    except ValueError as exc:
        # The checked-in model is stored in HDF5 format but uses a .keras suffix.
        if not (os.path.exists(model_path) and model_path.endswith(".keras")):
            raise

        with tempfile.NamedTemporaryFile(suffix=".h5", delete=False) as temp_model_file:
            temp_model_path = temp_model_file.name

        shutil.copyfile(model_path, temp_model_path)

        try:
            return tf.keras.models.load_model(temp_model_path)
        except Exception:
            raise exc
        finally:
            if os.path.exists(temp_model_path):
                os.remove(temp_model_path)

@st.cache_resource
def load_model_and_scalers():
    # Load model
    model = _load_legacy_compatible_model(
        os.path.join(
            path_models,
            "aapl_rnn_model.keras",
        )
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
