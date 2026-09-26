# 📊 Dataset Selection & Specification

## 1. Sales Dataset (`data/sales_data.csv`)

- **Description**: Historical transaction records covering sales orders across product categories, pricing, discounts, and regional distribution.
- **Record Count**: 1,200 rows.
- **Fields & Types**:

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `order_id` | String | Unique order identifier (e.g. `ORD-1001`) |
| `order_date` | Date | Date of order execution (`YYYY-MM-DD`) |
| `customer_id` | String | Customer identifier (e.g. `CUST-105`) |
| `region` | String | Geographic sales territory (`North America`, `Europe`, etc.) |
| `category` | String | Product category (`Electronics`, `Hardware`, `Software & Cloud`, `Office Supplies`) |
| `product_name` | String | Specific product name |
| `unit_price` | Float | Base product price ($) |
| `quantity` | Integer | Units ordered |
| `discount` | Float | Percentage discount applied |
| `sales` | Float | Net sales revenue ($) |
| `profit` | Float | Profit margin earned ($) |

---

## 2. User-Item Ratings Dataset (`data/user_ratings.csv`)

- **Description**: User rating evaluation matrix for products (scale 1 to 5 stars). Used for Collaborative Filtering recommendation modeling.
- **Fields**:
  - `user_id`: Integer ID of the user (1 to 10).
  - `item_id`: Integer ID of the item (101 to 110).
  - `rating`: Rating score (1.0 to 5.0).
