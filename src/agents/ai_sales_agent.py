"""
AI Sales Agent Engine.
Coordinates data analytics, forecasting, recommendations, and natural language query responses.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from src.agents.query_parser import QueryParser
from src.ml_models.collaborative_filtering import RecommendationAgent
from src.ml_models.sales_forecasting import SalesForecaster
from src.ml_models.customer_segmentation import CustomerSegmenter


class AISalesAgent:
    """Autonomous AI Agent for business analytics, ML predictions, and decision recommendations."""

    def __init__(self, sales_df: pd.DataFrame, ratings_df: pd.DataFrame):
        self.sales_df = sales_df.copy()
        self.ratings_df = ratings_df.copy()

        self.rec_agent = RecommendationAgent(self.ratings_df)
        self.forecaster = SalesForecaster(self.sales_df)
        self.segmenter = CustomerSegmenter(self.sales_df)

    def process_query(self, query_text: str) -> Dict[str, Any]:
        """Process natural language business query and return structured response & execution metadata."""
        parsed = QueryParser.parse_query(query_text)
        intent = parsed["intent"]

        response_data: Dict[str, Any] = {
            "query": query_text,
            "intent": intent,
            "execution_steps": [f"1. Parsed query intent as '{intent}'"],
            "answer": "",
            "table_data": None,
            "chart_type": None
        }

        if intent == "REVENUE_TOTAL":
            total_sales = self.sales_df["sales"].sum()
            total_profit = self.sales_df["profit"].sum()
            total_orders = self.sales_df["order_id"].nunique()
            margin = (total_profit / total_sales) * 100

            response_data["execution_steps"].append("2. Calculated aggregate sales metrics across whole dataset.")
            response_data["answer"] = (
                f"📊 **Financial Summary**:\n"
                f"- **Total Revenue**: ${total_sales:,.2f}\n"
                f"- **Total Profit**: ${total_profit:,.2f} (Profit Margin: {margin:.1f}%)\n"
                f"- **Total Orders Executed**: {total_orders:,}\n"
                f"- **Average Order Value (AOV)**: ${total_sales / total_orders:,.2f}"
            )

        elif intent == "TOP_PRODUCTS":
            top_n = parsed["top_n"]
            top_df = self.sales_df.groupby("product_name").agg({
                "sales": "sum",
                "profit": "sum",
                "quantity": "sum"
            }).sort_values("sales", ascending=False).head(top_n).reset_index()

            response_data["execution_steps"].append(f"2. Grouped sales by product_name and selected top {top_n}.")
            response_data["table_data"] = top_df
            response_data["chart_type"] = "bar"

            top_product = top_df.iloc[0]["product_name"]
            top_revenue = top_df.iloc[0]["sales"]
            response_data["answer"] = (
                f"🏆 **Top {top_n} Performing Products**:\n"
                f"- The #1 top-selling item is **{top_product}** generating **${top_revenue:,.2f}** in total revenue.\n"
                f"- Detailed breakdown shown in the table below."
            )

        elif intent == "CATEGORY_PERFORMANCE":
            cat_df = self.sales_df.groupby("category").agg({
                "sales": "sum",
                "profit": "sum",
                "order_id": "count"
            }).sort_values("sales", ascending=False).reset_index()
            cat_df["margin_pct"] = (cat_df["profit"] / cat_df["sales"] * 100).round(1)

            response_data["execution_steps"].append("2. Analyzed sales & profit margin across product categories.")
            response_data["table_data"] = cat_df
            response_data["chart_type"] = "pie"

            top_cat = cat_df.iloc[0]["category"]
            response_data["answer"] = (
                f"📦 **Category Breakdown**:\n"
                f"- Highest grossing category is **{top_cat}** with total revenue of **${cat_df.iloc[0]['sales']:,.2f}**.\n"
                f"- Highest margin category: **{cat_df.sort_values('margin_pct', ascending=False).iloc[0]['category']}** "
                f"({cat_df['margin_pct'].max()}%)"
            )

        elif intent == "SALES_FORECAST":
            days = parsed["days"]
            response_data["execution_steps"].append(f"2. Invoking Random Forest SalesForecaster for next {days} days.")

            metrics = self.forecaster.train()
            forecast_df = self.forecaster.forecast_next_days(days)
            total_forecasted = forecast_df["forecasted_sales"].sum()

            response_data["execution_steps"].append(f"3. Forecast model trained. MAE={metrics.get('MAE')}, R²={metrics.get('R2')}.")
            response_data["table_data"] = forecast_df
            response_data["chart_type"] = "line"
            response_data["answer"] = (
                f"🔮 **Sales Forecast ({days} Days)**:\n"
                f"- **Projected Revenue**: ${total_forecasted:,.2f}\n"
                f"- **Model Accuracy Metrics**: MAE = ${metrics.get('MAE'):,.2f} | R² Score = {metrics.get('R2')}\n"
                f"- Daily forecasted sales trends are visualized in the chart below."
            )

        elif intent == "RECOMMENDATION":
            user_id = parsed["user_id"]
            top_n = parsed["top_n"]
            response_data["execution_steps"].append(f"2. Querying Collaborative Filtering agent for User ID {user_id}.")

            recs = self.rec_agent.recommend(user_id=user_id, n=top_n)

            if recs:
                rec_df = pd.DataFrame(recs, columns=["item_id", "predicted_rating"])
                response_data["table_data"] = rec_df
                response_data["chart_type"] = "bar"
                response_data["answer"] = (
                    f"🎯 **Personalized Recommendations for User {user_id}**:\n"
                    f"- Top recommended item: **Item {recs[0][0]}** (Predicted Rating: {recs[0][1]} / 5.0).\n"
                    f"- Found {len(recs)} high-confidence item recommendations based on cosine item similarity."
                )
            else:
                response_data["answer"] = f"No recommendation history found for User ID {user_id}. Showing default recommendations."

        elif intent == "CUSTOMER_SEGMENT":
            response_data["execution_steps"].append("2. Running RFM & K-Means customer segmentation.")
            summary_df = self.segmenter.get_segment_summary()

            response_data["table_data"] = summary_df
            response_data["chart_type"] = "bar"
            response_data["answer"] = (
                f"👥 **Customer Segmentation Insights (RFM + K-Means)**:\n"
                f"- Customers divided into **4 distinct behavioral clusters**.\n"
                f"- Top revenue generating tier: **{summary_df.iloc[0]['Segment Name']}** "
                f"with total segment spend of **${summary_df.iloc[0]['Total Segment Revenue ($)']:,.2f}**."
            )

        else:
            total_sales = self.sales_df["sales"].sum()
            total_profit = self.sales_df["profit"].sum()

            response_data["execution_steps"].append("2. Generated executive overall summary.")
            response_data["answer"] = (
                f"🤖 **AI Executive Assistant Response**:\n"
                f"- **Total Platform Revenue**: ${total_sales:,.2f}\n"
                f"- **Total Net Profit**: ${total_profit:,.2f}\n"
                f"- Ask me specific questions like: *'What is our total revenue?'*, *'Show top 5 products'*, "
                f"*'Forecast sales for next 30 days'*, or *'Recommend items for user 1'*!"
            )

        return response_data
