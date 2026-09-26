"""
Collaborative Filtering Recommendation Agent.
Provides Item-Based and User-Based Recommendation capabilities.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple, Dict, Optional


class RecommendationAgent:
    """Item-Based Collaborative Filtering Recommendation Agent."""

    def __init__(self, ratings_df: pd.DataFrame):
        self.ratings_df = ratings_df.copy()
        self.user_item_matrix: Optional[pd.DataFrame] = None
        self.item_similarity: Optional[pd.DataFrame] = None
        self._fit()

    def _fit(self):
        """Construct user-item matrix and compute cosine similarity."""
        self.user_item_matrix = self.ratings_df.pivot_table(
            index="user_id",
            columns="item_id",
            values="rating"
        ).fillna(0)

        # Compute cosine similarity between item vectors
        sim = cosine_similarity(self.user_item_matrix.T)

        self.item_similarity = pd.DataFrame(
            sim,
            index=self.user_item_matrix.columns,
            columns=self.user_item_matrix.columns
        )

    def predict_rating(self, user_id: int, item_id: int, k: int = 3) -> float:
        """Predict user rating for a specific item using top-k similar items."""
        if item_id not in self.item_similarity.columns or user_id not in self.user_item_matrix.index:
            return np.nan

        user_ratings = self.user_item_matrix.loc[user_id]
        rated_items = user_ratings[user_ratings > 0]

        if rated_items.empty:
            return np.nan

        # Similarity scores between target item and items rated by user
        sims = self.item_similarity.loc[item_id, rated_items.index]
        top_k = sims.sort_values(ascending=False).head(k)

        if top_k.sum() == 0:
            return np.nan

        weighted_sum = (top_k * rated_items[top_k.index]).sum()
        predicted_rating = weighted_sum / top_k.sum()
        return round(float(predicted_rating), 2)

    def recommend(self, user_id: int, n: int = 5) -> List[Tuple[int, float]]:
        """Generate top-N item recommendations for a user."""
        if user_id not in self.user_item_matrix.index:
            return []

        user_ratings = self.user_item_matrix.loc[user_id]
        unrated_items = user_ratings[user_ratings == 0].index

        predictions: Dict[int, float] = {}
        for item in unrated_items:
            pred = self.predict_rating(user_id, item)
            if not np.isnan(pred):
                predictions[item] = pred

        ranked = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
        return ranked[:n]

    def get_user_item_matrix(self) -> pd.DataFrame:
        """Return the pivot user-item matrix."""
        return self.user_item_matrix

    def get_similarity_matrix(self) -> pd.DataFrame:
        """Return item similarity DataFrame."""
        return self.item_similarity
