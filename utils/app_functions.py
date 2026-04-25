from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

try:
    import tensorflow as tf
except ImportError:  # pragma: no cover - exercised in lightweight runtime setups
    tf = None


ROOT_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = ROOT_DIR / "models"
DATA_FILE = ROOT_DIR / "data" / "processed" / "aapl_data.csv"
MODEL_FILE = MODELS_DIR / "aapl_rnn_model.keras"
TARGET_SCALER_FILE = MODELS_DIR / "aapl_target_scaler.pkl"
FEATURE_SCALER_FILE = MODELS_DIR / "aapl_feature_scaler.pkl"
REQUIRED_COLUMNS = ["Date", "AAPL", "AAPL_target", "negative", "neutral", "positive"]
SEQUENCE_LENGTH = 30


@st.cache_data
def build_demo_data() -> pd.DataFrame:
    """Generate a lightweight demo dataset when the trained assets are unavailable."""
    dates = pd.bdate_range(start="2024-01-02", end="2025-12-31")
    index = np.arange(len(dates), dtype=float)

    positive = 0.30 + (0.08 * np.sin(index / 11))
    negative = 0.22 + (0.06 * np.cos(index / 13))
    neutral = 1 - positive - negative

    aapl = 175 + (0.12 * index) + (3.5 * np.sin(index / 7)) + (2.2 * (positive - negative))
    aapl = np.round(aapl, 2)
    aapl_target = np.roll(aapl, -1)
    aapl_target[-1] = aapl[-1]

    return pd.DataFrame(
        {
            "Date": dates.date,
            "AAPL": aapl,
            "AAPL_target": np.round(aapl_target, 2),
            "negative": np.round(negative, 4),
            "neutral": np.round(neutral, 4),
            "positive": np.round(positive, 4),
        }
    )


def _normalize_data(data: pd.DataFrame) -> pd.DataFrame:
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing_columns:
        raise ValueError(
            "The dataset is missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    normalized = data.copy()
    normalized["Date"] = pd.to_datetime(normalized["Date"]).dt.date
    normalized = normalized.sort_values("Date").drop_duplicates("Date", keep="last")
    return normalized.reset_index(drop=True)


@st.cache_data
def load_price_data() -> tuple[pd.DataFrame, str | None]:
    """Load the project dataset when available, otherwise fall back to demo data."""
    if DATA_FILE.exists():
        try:
            return _normalize_data(pd.read_csv(DATA_FILE)), None
        except Exception as exc:
            return (
                _normalize_data(build_demo_data()),
                "The processed dataset could not be loaded "
                f"({exc.__class__.__name__}). Showing bundled demo data instead.",
            )

    return (
        _normalize_data(build_demo_data()),
        "The processed dataset was not found. Showing bundled demo data instead.",
    )


@st.cache_resource
def load_model_and_scalers():
    """Load the trained model artifacts when they are present and usable."""
    if tf is None:
        return None, None, None, "TensorFlow is not installed. Using demo forecast mode."

    required_files = [MODEL_FILE, TARGET_SCALER_FILE, FEATURE_SCALER_FILE]
    missing_files = [str(path.relative_to(ROOT_DIR)) for path in required_files if not path.exists()]
    if missing_files:
        return (
            None,
            None,
            None,
            "The trained model artifacts are missing ("
            + ", ".join(missing_files)
            + "). Using demo forecast mode.",
        )

    try:
        model = tf.keras.models.load_model(MODEL_FILE)

        with TARGET_SCALER_FILE.open("rb") as target_scaler_file:
            target_scaler = pickle.load(target_scaler_file)

        with FEATURE_SCALER_FILE.open("rb") as feature_scaler_file:
            feature_scaler = pickle.load(feature_scaler_file)
    except Exception as exc:
        return (
            None,
            None,
            None,
            "The trained model could not be loaded "
            f"({exc.__class__.__name__}). Using demo forecast mode.",
        )

    return model, target_scaler, feature_scaler, None


def get_prediction_mode_message() -> str | None:
    _, _, _, message = load_model_and_scalers()
    return message


def _fallback_predict(data_predict: pd.DataFrame) -> float:
    recent_window = data_predict.tail(SEQUENCE_LENGTH).copy()
    last_price = float(recent_window.iloc[-1]["AAPL"])

    average_pct_move = recent_window["AAPL"].pct_change().dropna().tail(5).mean()
    if pd.isna(average_pct_move):
        average_pct_move = 0.0

    sentiment_bias = (
        recent_window[["positive", "negative"]]
        .tail(5)
        .assign(sentiment_gap=lambda frame: frame["positive"] - frame["negative"])["sentiment_gap"]
        .mean()
        * 0.01
    )

    predicted_price = last_price * (1 + average_pct_move + sentiment_bias)
    return float(max(round(predicted_price, 2), 0.01))


def predict(data: pd.DataFrame, selected_date) -> float:
    data_predict = data[data["Date"] <= selected_date].copy()
    if data_predict.empty:
        raise ValueError("No data is available for the selected date.")

    model, target_scaler, feature_scaler, _ = load_model_and_scalers()
    if (
        model is None
        or target_scaler is None
        or feature_scaler is None
        or data_predict.shape[0] <= SEQUENCE_LENGTH
    ):
        return _fallback_predict(data_predict)

    data_predict["AAPL_target"] = target_scaler.transform(data_predict[["AAPL_target"]])
    data_predict["AAPL"] = feature_scaler.transform(data_predict[["AAPL"]])

    features = ["AAPL", "negative", "neutral", "positive"]
    sequences = []
    for index in range(SEQUENCE_LENGTH, data_predict.shape[0]):
        sequences.append(data_predict[features].iloc[index - SEQUENCE_LENGTH : index])

    X = np.array(sequences)
    y_pred = model.predict(X, verbose=0)
    prediction = target_scaler.inverse_transform(y_pred)
    return float(prediction[-1, -1])


def compute_predicted_date(available_dates: list, selected_date):
    predicted_date = next((date for date in available_dates if date > selected_date), None)
    if predicted_date is None:
        raise ValueError("Choose a date before the last available trading day.")

    return predicted_date
