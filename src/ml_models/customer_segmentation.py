"""
Customer Behavioral Segmentation ML Model.
Applies RFM (Recency, Frequency, Monetary) analysis and K-Means clustering.
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any, Tuple


class CustomerSegmenter:
    """RFM & K-Means Customer Clustering Engine."""

    def __init__(self, sales_df: pd.DataFrame, n_clusters: int = 4):
        self.sales_df = sales_df.copy()
        self.n_clusters = n_clusters
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.rfm_df: pd.DataFrame = pd.DataFrame()

    def fit_transform(self) -> pd.DataFrame:
        """Calculate RFM features and fit K-Means clustering."""
        self.sales_df["order_date"] = pd.to_datetime(self.sales_df["order_date"])
        max_date = self.sales_df["order_date"].max() + pd.Timedelta(days=1)

        # Aggregate RFM per customer
        rfm = self.sales_df.groupby("customer_id").agg({
            "order_date": lambda dates: (max_date - dates.max()).days,
            "order_id": "nunique",
            "sales": "sum"
        }).reset_index()

        rfm.columns = ["customer_id", "recency", "frequency", "monetary"]

        # Scale features
        rfm_scaled = self.scaler.fit_transform(rfm[["recency", "frequency", "monetary"]])
        rfm["cluster"] = self.kmeans.fit_predict(rfm_scaled)

        # Map cluster labels to meaningful persona names based on average monetary value
        cluster_monetary = rfm.groupby("cluster")["monetary"].mean().sort_values(ascending=False)
        persona_map = {}
        labels = ["VIP Champions", "Loyal Spenders", "Steady Customers", "At-Risk / Low Volume"]

        for idx, (cluster_id, _) in enumerate(cluster_monetary.items()):
            persona_map[cluster_id] = labels[min(idx, len(labels) - 1)]

        rfm["segment_name"] = rfm["cluster"].map(persona_map)
        self.rfm_df = rfm
        return rfm

    def get_segment_summary(self) -> pd.DataFrame:
        """Return summary statistics for each segment."""
        if self.rfm_df.empty:
            self.fit_transform()

        summary = self.rfm_df.groupby("segment_name").agg({
            "customer_id": "count",
            "recency": "mean",
            "frequency": "mean",
            "monetary": ["mean", "sum"]
        }).reset_index()

        summary.columns = [
            "Segment Name",
            "Customer Count",
            "Avg Recency (Days)",
            "Avg Orders",
            "Avg Spend ($)",
            "Total Segment Revenue ($)"
        ]

        summary["Avg Recency (Days)"] = summary["Avg Recency (Days)"].round(1)
        summary["Avg Orders"] = summary["Avg Orders"].round(1)
        summary["Avg Spend ($)"] = summary["Avg Spend ($)"].round(2)
        summary["Total Segment Revenue ($)"] = summary["Total Segment Revenue ($)"].round(2)

        return summary
