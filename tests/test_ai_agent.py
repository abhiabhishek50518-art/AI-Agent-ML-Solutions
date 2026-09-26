"""
Unit tests for AI Sales Agent engine.
"""

import pytest
import pandas as pd
import numpy as np
from src.agents.ai_sales_agent import AISalesAgent


@pytest.fixture
def agent_environment():
    dates = pd.date_range("2024-01-01", periods=60)
    sales_data = []
    for d in dates:
        sales_data.append({
            "order_id": f"ORD-{d.strftime('%Y%m%d')}",
            "order_date": d.strftime("%Y-%m-%d"),
            "customer_id": "CUST-101",
            "region": "North America",
            "category": "Electronics",
            "product_name": "Laptop Pro",
            "unit_price": 1200,
            "quantity": 2,
            "discount": 0.0,
            "sales": 2400.0,
            "profit": 480.0
        })
    sales_df = pd.DataFrame(sales_data)

    ratings_df = pd.DataFrame({
        "user_id": [1, 1, 1, 2, 2, 2],
        "item_id": [101, 102, 103, 101, 103, 104],
        "rating": [5, 3, 4, 4, 5, 2]
    })

    return AISalesAgent(sales_df, ratings_df)


def test_agent_total_revenue_query(agent_environment):
    res = agent_environment.process_query("What is our total revenue?")
    assert res["intent"] == "REVENUE_TOTAL"
    assert "Financial Summary" in res["answer"]
    assert len(res["execution_steps"]) >= 2


def test_agent_top_products_query(agent_environment):
    res = agent_environment.process_query("Show me top 5 selling products")
    assert res["intent"] == "TOP_PRODUCTS"
    assert res["table_data"] is not None
    assert "Laptop Pro" in res["answer"]


def test_agent_forecast_query(agent_environment):
    res = agent_environment.process_query("Forecast sales for next 30 days")
    assert res["intent"] == "SALES_FORECAST"
    assert res["table_data"] is not None
    assert len(res["table_data"]) == 30


def test_agent_recommendation_query(agent_environment):
    res = agent_environment.process_query("Recommend items for user 1")
    assert res["intent"] == "RECOMMENDATION"
    assert "Personalized Recommendations" in res["answer"]
