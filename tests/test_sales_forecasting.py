"""
Unit tests for SalesForecaster ML model.
"""

import pytest
import pandas as pd
import numpy as np
from src.ml_models.sales_forecasting import SalesForecaster


@pytest.fixture
def sample_sales_df():
    dates = pd.date_range("2024-01-01", periods=60)
    data = []
    for d in dates:
        data.append({
            "order_date": d.strftime("%Y-%m-%d"),
            "sales": np.random.uniform(500, 2000),
            "profit": np.random.uniform(100, 500),
            "quantity": np.random.randint(1, 10)
        })
    return pd.DataFrame(data)


def test_sales_forecaster_training(sample_sales_df):
    forecaster = SalesForecaster(sample_sales_df)
    metrics = forecaster.train()
    assert "MAE" in metrics
    assert "RMSE" in metrics
    assert "R2" in metrics
    assert metrics["MAE"] >= 0


def test_sales_forecaster_forecast(sample_sales_df):
    forecaster = SalesForecaster(sample_sales_df)
    forecast_df = forecaster.forecast_next_days(days=14)
    assert len(forecast_df) == 14
    assert "date" in forecast_df.columns
    assert "forecasted_sales" in forecast_df.columns
    assert (forecast_df["forecasted_sales"] >= 0).all()
