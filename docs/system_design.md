# 🏗️ System Design & Architecture Specification

## Overview

The **AI Agent & Machine Learning Solutions Platform** is engineered with a modular, decoupled 3-tier architecture:
1. **User Interface Tier**: Multi-tab Streamlit dashboard (`src/dashboard/app.py`).
2. **Autonomous Agent & Tool Execution Tier**: Query parser, routing engine, multi-tool orchestrator (`src/agents/`).
3. **Machine Learning & Analytical Engine Tier**: Collaborative Filtering recommendation agent, Random Forest time-series forecaster, RFM K-Means customer segmenter (`src/ml_models/`).

---

## 📐 Architecture Diagram

```
+-----------------------------------------------------------------------+
|                      User Interface (Streamlit)                       |
|   Analytics Dashboard | AI Chat Agent | Recommendations | Forecasts    |
+-----------------------------------+-----------------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                       Autonomous AI Agent Layer                       |
|   QueryParser (Intent Regex) <----> AISalesAgent Multi-Tool Router    |
+----------+------------------------+------------------------+----------+
           |                        |                        |
           v                        v                        v
+-----------------------+ +--------------------+ +----------------------+
| Recommendation Agent  | |  Sales Forecaster  | | Customer Segmenter   |
| Cosine Similarity Matrix| | Random Forest ML | | RFM K-Means Cluster  |
+-----------------------+ +--------------------+ +----------------------+
           |                        |                        |
           +------------------------+------------------------+
                                    |
                                    v
+-----------------------------------------------------------------------+
|                         Data Layer (Pandas)                           |
|       sales_data.csv (1200 records)  |  user_ratings.csv (Matrix)     |
+-----------------------------------------------------------------------+
```

---

## 🧩 Component Specifications

### 1. Recommendation Agent (`collaborative_filtering.py`)
- **Algorithm**: Item-Based Collaborative Filtering using Cosine Similarity.
- **Formulas**:
  - Cosine Similarity:
    $$\text{Sim}(i, j) = \frac{\mathbf{v}_i \cdot \mathbf{v}_j}{\|\mathbf{v}_i\| \|\mathbf{v}_j\|}$$
  - Weighted Predicted Rating:
    $$\hat{r}_{u, i} = \frac{\sum_{j \in TopK} \text{Sim}(i, j) \cdot r_{u, j}}{\sum_{j \in TopK} \text{Sim}(i, j)}$$

### 2. Sales Forecaster (`sales_forecasting.py`)
- **Algorithm**: Random Forest Regressor time-series model ($N_{estimators}=100$).
- **Features**: Lag 1 day sales, Lag 7 day sales, 7-day rolling mean, Day-of-week, Day-of-month, Month, Quarter.
- **Validation**: 80/20 sequential time-series train/test split. Evaluation metrics ($MAE$, $RMSE$, $R^2$).

### 3. Customer Segmenter (`customer_segmentation.py`)
- **Methodology**: RFM (Recency, Frequency, Monetary) metrics calculation followed by $K$-Means clustering ($k=4$).
- **Personas**: VIP Champions, Loyal Spenders, Steady Customers, At-Risk / Low Volume.
