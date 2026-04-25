import datetime as dt

import pandas as pd
import pytest

from utils.app_functions import (
    ModelArtifactsError,
    MissingModelArtifactsError,
    compute_predicted_date,
    fallback_predict,
    load_model_and_scalers,
    missing_model_artifacts,
)


def test_load_model_reports_missing_artifacts(monkeypatch, tmp_path):
    import utils.app_functions as app_functions

    monkeypatch.setattr(app_functions, "path_models", str(tmp_path))
    load_model_and_scalers.clear()
    missing_files = missing_model_artifacts()

    assert missing_files
    with pytest.raises(MissingModelArtifactsError) as exc_info:
        load_model_and_scalers()

    assert exc_info.value.missing_files == missing_files


def test_load_model_wraps_unreadable_artifacts(monkeypatch, tmp_path):
    model_dir = tmp_path / "models"
    model_dir.mkdir()
    for file_name in ("aapl_rnn_model.keras", "aapl_target_scaler.pkl", "aapl_feature_scaler.pkl"):
        (model_dir / file_name).write_text("not a valid model artifact")

    monkeypatch.setattr("utils.app_functions.path_models", str(model_dir))

    with pytest.raises(ModelArtifactsError):
        load_model_and_scalers()


def test_fallback_predict_uses_target_when_available():
    data = pd.DataFrame(
        {
            "Date": [dt.date(2024, 1, 1), dt.date(2024, 1, 2)],
            "AAPL": [100.0, 101.0],
            "AAPL_target": [101.0, 102.5],
        }
    )

    assert fallback_predict(data, dt.date(2024, 1, 2)) == 102.5


def test_compute_predicted_date_uses_available_dates():
    available_dates = [
        dt.date(2024, 1, 1),
        dt.date(2024, 1, 3),
        dt.date(2024, 1, 5),
    ]

    predicted_date = compute_predicted_date(
        min_date=dt.date(2024, 1, 1),
        max_date=dt.date(2024, 1, 5),
        selected_date=dt.date(2024, 1, 3),
        available_dates=available_dates,
    )

    assert predicted_date == dt.date(2024, 1, 5)


def test_compute_predicted_date_returns_none_without_future_dates():
    available_dates = [dt.date(2024, 1, 1), dt.date(2024, 1, 3)]

    predicted_date = compute_predicted_date(
        min_date=dt.date(2024, 1, 1),
        max_date=dt.date(2024, 1, 3),
        selected_date=dt.date(2024, 1, 3),
        available_dates=available_dates,
    )

    assert predicted_date is None
