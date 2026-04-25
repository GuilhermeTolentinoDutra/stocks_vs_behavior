import pickle
import numpy as np
import os
import pandas as pd
import streamlit as st
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

path_models = os.path.join(os.path.abspath(""), "models")
MODEL_FILE = "aapl_rnn_model.keras"
TARGET_SCALER_FILE = "aapl_target_scaler.pkl"
FEATURE_SCALER_FILE = "aapl_feature_scaler.pkl"
REQUIRED_MODEL_FILES = (MODEL_FILE, TARGET_SCALER_FILE, FEATURE_SCALER_FILE)


class ModelArtifactsError(RuntimeError):
    """Base class for model artifact availability problems."""


class MissingModelArtifactsError(ModelArtifactsError, FileNotFoundError):
    """Raised when the trained model artifacts are not available locally."""

    def __init__(self, missing_files):
        self.missing_files = missing_files
        files = ", ".join(missing_files)
        super().__init__(
            f"Missing model artifacts in {path_models}: {files}. "
            "Add the trained files or use the fallback prediction."
        )


class ModelArtifactLoadError(ModelArtifactsError):
    """Raised when model artifacts exist but cannot be loaded."""


def missing_model_artifacts():
    return [
        file_name
        for file_name in REQUIRED_MODEL_FILES
        if not os.path.exists(os.path.join(path_models, file_name))
    ]


@st.cache_resource
def load_model_and_scalers():
    missing_files = missing_model_artifacts()
    if missing_files:
        raise MissingModelArtifactsError(missing_files)

    import tensorflow as tf

    try:
        # Load model
        model = tf.keras.models.load_model(
            os.path.join(
                path_models,
                MODEL_FILE,
            )
        )

        # Load scaler applied to target column
        with open(os.path.join(path_models, TARGET_SCALER_FILE), "rb") as f:
            target_scaler = pickle.load(f)

        with open(os.path.join(path_models, FEATURE_SCALER_FILE), "rb") as f:
            feature_scaler = pickle.load(f)
    except (OSError, ValueError, pickle.PickleError) as exc:
        raise ModelArtifactLoadError(
            "The trained model artifacts could not be loaded. "
            "Regenerate them with the current Keras/scikit-learn versions "
            "or use the fallback prediction."
        ) from exc

    return model, target_scaler, feature_scaler


def predict(data, selected_date):
    model, target_scaler, feature_scaler = load_model_and_scalers()

    # selected_date = selected_date + " 23:59:59"
    data_predict = data[data["Date"] <= selected_date].copy()
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


def fallback_predict(data, selected_date):
    data_predict = data[data["Date"] <= selected_date].sort_values("Date")
    if data_predict.empty:
        raise ValueError("No price history is available for the selected date.")

    latest_row = data_predict.iloc[-1]
    if "AAPL_target" in latest_row and not pd.isna(latest_row["AAPL_target"]):
        return float(latest_row["AAPL_target"])

    return float(latest_row["AAPL"])


def compute_predicted_date(min_date, max_date, selected_date, available_dates=None):
    if available_dates is not None:
        available_dates = pd.to_datetime(pd.Series(available_dates)).dt.date
        future_dates = available_dates[available_dates > selected_date].sort_values()
        if future_dates.empty:
            return None

        return future_dates.iloc[0]

    calendar = pd.DataFrame(
        pd.date_range(
            start=min_date,
            end=max_date,
            freq=CustomBusinessDay(calendar=USFederalHolidayCalendar()),
        ),
        columns=["Date"],
    )

    calendar["Date"] = pd.to_datetime(calendar["Date"]).dt.date

    future_dates = calendar[calendar["Date"] > selected_date]
    if future_dates.empty:
        return None

    predicted_date = pd.to_datetime(future_dates.iloc[0]["Date"]).date()

    return predicted_date
