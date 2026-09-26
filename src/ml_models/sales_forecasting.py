"""
Sales Forecasting ML Model.
Provides Time Series & Regression-based forecasting for future sales and revenue.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score
from typing import Dict, Any, Tuple


class SalesForecaster:
    """Sales Forecasting ML Model for revenue and demand predictions."""

    def __init__(self, sales_df: pd.DataFrame):
        self.sales_df = sales_df.copy()
        self.sales_df["order_date"] = pd.to_datetime(self.sales_df["order_date"])
        self.daily_sales: pd.DataFrame = pd.DataFrame()
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.is_trained = False
        self._prepare_features()

    def _prepare_features(self):
        """Aggregate daily sales and extract temporal features."""
        daily = self.sales_df.groupby("order_date").agg({
            "sales": "sum",
            "profit": "sum",
            "quantity": "sum"
        }).reset_index()

        daily = daily.sort_values("order_date").reset_index(drop=True)

        daily["day_of_week"] = daily["order_date"].dt.dayofweek
        daily["day_of_month"] = daily["order_date"].dt.day
        daily["month"] = daily["order_date"].dt.month
        daily["quarter"] = daily["order_date"].dt.quarter
        daily["lag_1"] = daily["sales"].shift(1)
        daily["lag_7"] = daily["sales"].shift(7)
        daily["rolling_7_mean"] = daily["sales"].shift(1).rolling(window=7).mean()

        daily = daily.dropna().reset_index(drop=True)
        self.daily_sales = daily

    def train(self) -> Dict[str, float]:
        """Train the forecasting model and return evaluation metrics."""
        if len(self.daily_sales) < 15:
            return {"status": "error", "message": "Insufficient data points"}

        X = self.daily_sales[["day_of_week", "day_of_month", "month", "quarter", "lag_1", "lag_7", "rolling_7_mean"]]
        y = self.daily_sales["sales"]

        split_idx = int(len(X) * 0.8)
        X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        rmse = root_mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        self.is_trained = True

        # Retrain on full dataset
        self.model.fit(X, y)

        return {
            "MAE": round(float(mae), 2),
            "RMSE": round(float(rmse), 2),
            "R2": round(float(r2), 4)
        }

    def forecast_next_days(self, days: int = 30) -> pd.DataFrame:
        """Forecast sales for the next N days into the future."""
        if not self.is_trained:
            self.train()

        last_date = self.daily_sales["order_date"].max()
        last_sales = list(self.daily_sales["sales"].values[-14:])

        forecasts = []

        for i in range(1, days + 1):
            next_date = last_date + pd.Timedelta(days=i)
            dow = next_date.dayofweek
            dom = next_date.day
            month = next_date.month
            quarter = next_date.quarter

            lag_1 = last_sales[-1]
            lag_7 = last_sales[-7] if len(last_sales) >= 7 else last_sales[0]
            rolling_7 = np.mean(last_sales[-7:])

            feat = pd.DataFrame([{
                "day_of_week": dow,
                "day_of_month": dom,
                "month": month,
                "quarter": quarter,
                "lag_1": lag_1,
                "lag_7": lag_7,
                "rolling_7_mean": rolling_7
            }])

            pred_sales = max(0.0, float(self.model.predict(feat)[0]))
            forecasts.append({
                "date": next_date.strftime("%Y-%m-%d"),
                "forecasted_sales": round(pred_sales, 2)
            })
            last_sales.append(pred_sales)

        return pd.DataFrame(forecasts)
