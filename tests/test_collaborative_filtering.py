"""
Unit tests for Collaborative Filtering Recommendation Agent.
"""

import pytest
import pandas as pd
import numpy as np
from src.ml_models.collaborative_filtering import RecommendationAgent


@pytest.fixture
def sample_ratings_df():
    return pd.DataFrame({
        "user_id": [1, 1, 1, 2, 2, 2, 3, 3],
        "item_id": [101, 102, 103, 101, 103, 104, 102, 104],
        "rating": [5, 3, 4, 4, 5, 2, 5, 3]
    })


def test_fit_matrix(sample_ratings_df):
    agent = RecommendationAgent(sample_ratings_df)
    matrix = agent.get_user_item_matrix()
    assert matrix.shape == (3, 4)
    assert 101 in matrix.columns
    assert 1 in matrix.index


def test_similarity_matrix(sample_ratings_df):
    agent = RecommendationAgent(sample_ratings_df)
    sim = agent.get_similarity_matrix()
    assert sim.shape == (4, 4)
    # Self similarity should be 1.0
    assert pytest.approx(sim.loc[101, 101], 0.01) == 1.0


def test_predict_rating(sample_ratings_df):
    agent = RecommendationAgent(sample_ratings_df)
    # User 1 hasn't rated item 104
    predicted = agent.predict_rating(user_id=1, item_id=104)
    assert not np.isnan(predicted)
    assert 1.0 <= predicted <= 5.0


def test_recommend_items(sample_ratings_df):
    agent = RecommendationAgent(sample_ratings_df)
    recs = agent.recommend(user_id=1, n=2)
    assert isinstance(recs, list)
    assert len(recs) >= 1
    item_id, score = recs[0]
    assert item_id == 104
    assert score > 0
