"""
Query Parser and Intent Classification Engine for AI Sales Agent.
"""

import re
from typing import Dict, Any


class QueryParser:
    """Parses natural language business questions into structured intents and parameters."""

    INTENTS = {
        "REVENUE_TOTAL": [r"total revenue", r"total sales", r"overall sales", r"how much money"],
        "TOP_PRODUCTS": [r"top.*product", r"top.*selling", r"best.*selling", r"most.*sold", r"highest sales"],
        "CATEGORY_PERFORMANCE": [r"category", r"categories", r"which category", r"profit by category"],
        "SALES_FORECAST": [r"forecast", r"predict", r"future sales", r"next month", r"next \d+ days"],
        "RECOMMENDATION": [r"recommend", r"recommendation", r"suggest items", r"item rating", r"what to buy"],
        "CUSTOMER_SEGMENT": [r"customer segment", r"rfm", r"top customers", r"customer cluster", r"vip customers"],
        "PROFIT_ANALYSIS": [r"profit", r"margin", r"highest profit", r"most profitable"]
    }

    @classmethod
    def parse_query(cls, query_text: str) -> Dict[str, Any]:
        """Classify query text and extract parameters."""
        text_lower = query_text.lower().strip()

        matched_intent = "GENERAL_SUMMARY"
        for intent, patterns in cls.INTENTS.items():
            if any(re.search(pattern, text_lower) for pattern in patterns):
                matched_intent = intent
                break

        # Extract numerical parameters if available (e.g., user_id=1, top 5)
        user_match = re.search(r"user\s*(\d+)", text_lower)
        user_id = int(user_match.group(1)) if user_match else 1

        top_n_match = re.search(r"top\s*(\d+)", text_lower)
        top_n = int(top_n_match.group(1)) if top_n_match else 5

        days_match = re.search(r"(\d+)\s*days", text_lower)
        days = int(days_match.group(1)) if days_match else 30

        return {
            "query": query_text,
            "intent": matched_intent,
            "user_id": user_id,
            "top_n": top_n,
            "days": days
        }
