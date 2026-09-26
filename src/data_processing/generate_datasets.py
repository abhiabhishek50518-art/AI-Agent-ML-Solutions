"""
Data generation module for AI Agent & Machine Learning Solutions.
Generates realistic Sales Dataset and User-Item Rating Dataset.
"""

import os
import numpy as np
import pandas as pd


def generate_sales_dataset(output_path: str, num_records: int = 1200) -> pd.DataFrame:
    """Generate realistic sales transactions dataset."""
    np.random.seed(42)
    start_date = pd.to_datetime("2024-01-01")

    categories = {
        "Electronics": ["Laptop Pro", "Wireless Headphone", "Smart Watch", "Ultra Monitor", "Tablet Air"],
        "Office Supplies": ["Ergonomic Chair", "Standing Desk", "Mechanical Keyboard", "LED Desk Lamp", "Paper Shredder"],
        "Software & Cloud": ["SaaS Enterprise License", "Cloud Storage Pro", "AI Analytics Suite", "Security Vault", "CRM Standard"],
        "Hardware": ["NVMe SSD 1TB", "Graphics Card RTX", "Power Supply 850W", "RAM Kit 32GB", "Motherboard Z790"]
    }

    regions = ["North America", "Europe", "Asia-Pacific", "Latin America"]

    records = []
    for i in range(num_records):
        order_id = f"ORD-{1000 + i}"
        days_offset = np.random.randint(0, 365)
        order_date = start_date + pd.Timedelta(days=days_offset)

        category = np.random.choice(list(categories.keys()))
        product = np.random.choice(categories[category])

        base_prices = {
            "Laptop Pro": 1200, "Wireless Headphone": 150, "Smart Watch": 250, "Ultra Monitor": 450, "Tablet Air": 600,
            "Ergonomic Chair": 350, "Standing Desk": 550, "Mechanical Keyboard": 120, "LED Desk Lamp": 45, "Paper Shredder": 90,
            "SaaS Enterprise License": 2500, "Cloud Storage Pro": 300, "AI Analytics Suite": 1800, "Security Vault": 750, "CRM Standard": 450,
            "NVMe SSD 1TB": 110, "Graphics Card RTX": 850, "Power Supply 850W": 140, "RAM Kit 32GB": 130, "Motherboard Z790": 280
        }

        unit_price = base_prices[product]
        quantity = np.random.randint(1, 10)
        discount = round(np.random.choice([0.0, 0.05, 0.1, 0.15, 0.2]), 2)

        sales = round(unit_price * quantity * (1 - discount), 2)
        margin_pct = np.random.uniform(0.15, 0.45)
        profit = round(sales * margin_pct, 2)
        customer_id = f"CUST-{np.random.randint(100, 250)}"
        region = np.random.choice(regions, p=[0.4, 0.3, 0.2, 0.1])

        records.append({
            "order_id": order_id,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "customer_id": customer_id,
            "region": region,
            "category": category,
            "product_name": product,
            "unit_price": unit_price,
            "quantity": quantity,
            "discount": discount,
            "sales": sales,
            "profit": profit
        })

    df = pd.DataFrame(records)
    df = df.sort_values("order_date").reset_index(drop=True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


def generate_ratings_dataset(output_path: str) -> pd.DataFrame:
    """Generate User-Item ratings matrix for Collaborative Filtering agent."""
    np.random.seed(42)
    users = list(range(1, 11))
    items = list(range(101, 111))

    records = []
    for u in users:
        # Each user rates 4 to 8 items
        num_ratings = np.random.randint(4, 9)
        rated_items = np.random.choice(items, size=num_ratings, replace=False)
        for item in rated_items:
            rating = np.random.choice([1, 2, 3, 4, 5], p=[0.05, 0.1, 0.25, 0.35, 0.25])
            records.append({"user_id": u, "item_id": item, "rating": rating})

    df = pd.DataFrame(records)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    sales_path = "C:/Users/racha/OneDrive/Desktop/AI agents ML Solutions/data/sales_data.csv"
    ratings_path = "C:/Users/racha/OneDrive/Desktop/AI agents ML Solutions/data/user_ratings.csv"
    generate_sales_dataset(sales_path)
    generate_ratings_dataset(ratings_path)
    print(f"Generated sales dataset at {sales_path}")
    print(f"Generated ratings dataset at {ratings_path}")
