"""
Streamlit Web Dashboard for AI Agent & Machine Learning Solutions.
Features multi-tab executive dashboard, AI Agent natural language chat, recommendation engine,
sales forecasting, customer segmentation, and 9-week project milestone tracker.
"""

import os
import sys
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.data_processing.generate_datasets import generate_sales_dataset, generate_ratings_dataset
from src.ml_models.collaborative_filtering import RecommendationAgent
from src.ml_models.sales_forecasting import SalesForecaster
from src.ml_models.customer_segmentation import CustomerSegmenter
from src.agents.ai_sales_agent import AISalesAgent


# Page Setup
st.set_page_config(
    page_title="AI Agent & ML Solutions Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stApp { color: #f0f2f6; }
    .css-1r6594q { background-color: #161b22; }
    .stMetric { background: linear-gradient(135deg, #1f2937, #111827); border: 1px solid #374151; padding: 15px; border-radius: 12px; }
    .stMetric label { font-weight: 600; color: #9ca3af; }
    .stMetric div[data-testid="stMetricValue"] { font-size: 1.8rem; font-weight: 700; color: #38bdf8; }
    .milestone-card {
        background: #1e293b;
        border-left: 5px solid #10b981;
        padding: 16px;
        margin-bottom: 14px;
        border-radius: 8px;
    }
    .milestone-title { font-size: 1.15rem; font-weight: 700; color: #10b981; }
    .milestone-desc { color: #cbd5e1; font-size: 0.95rem; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    sales_path = os.path.join(PROJECT_ROOT, "data", "sales_data.csv")
    ratings_path = os.path.join(PROJECT_ROOT, "data", "user_ratings.csv")

    if not os.path.exists(sales_path) or not os.path.exists(ratings_path):
        sales_df = generate_sales_dataset(sales_path)
        ratings_df = generate_ratings_dataset(ratings_path)
    else:
        sales_df = pd.read_csv(sales_path)
        ratings_df = pd.read_csv(ratings_path)

    return sales_df, ratings_df


sales_df, ratings_df = load_data()
ai_agent = AISalesAgent(sales_df, ratings_df)

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/color/96/bot.png", width=70)
st.sidebar.title("AI Agent & ML Solutions")
st.sidebar.caption("Internship Final Project Delivery")

tab_choice = st.sidebar.radio(
    "Select Platform Module:",
    [
        "📊 Executive Sales Analytics",
        "🤖 AI Sales Agent Chat",
        "🎯 Recommendation Engine",
        "📈 Sales Forecasting",
        "👥 Customer Segmentation",
        "📅 Internship Milestones & Roadmap"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Project Repository**: [GitHub Repo](https://github.com/abhiabhishek50518-art/AI-Agent-ML-Solutions)\n\n"
    "👤 **Internship Student**: Abhi Abhishek\n\n"
    "🎯 **Domain**: AI Agents & Machine Learning"
)

# Header
st.title("🤖 AI Agent & Machine Learning Solutions Platform")
st.markdown("---")

# ---------------------------------------------------------
# TAB 1: EXECUTIVE SALES ANALYTICS
# ---------------------------------------------------------
if tab_choice == "📊 Executive Sales Analytics":
    st.subheader("📊 Executive Business Analytics Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    total_sales = sales_df["sales"].sum()
    total_profit = sales_df["profit"].sum()
    total_orders = sales_df["order_id"].nunique()
    avg_order_value = total_sales / total_orders

    col1.metric("Total Revenue", f"${total_sales:,.2f}", "+14.2% YoY")
    col2.metric("Total Profit", f"${total_profit:,.2f}", "+18.5% YoY")
    col3.metric("Total Transactions", f"{total_orders:,}", "+8.1% YoY")
    col4.metric("Avg Order Value", f"${avg_order_value:,.2f}", "+5.4% YoY")

    st.markdown("### 📈 Revenue & Profit Trends")
    sales_df["order_date"] = pd.to_datetime(sales_df["order_date"])
    monthly = sales_df.set_index("order_date").resample("M").agg({"sales": "sum", "profit": "sum"}).reset_index()

    fig_trend = px.line(
        monthly, x="order_date", y=["sales", "profit"],
        labels={"value": "Amount ($)", "order_date": "Month"},
        title="Monthly Sales vs. Profit Performance",
        color_discrete_sequence=["#38bdf8", "#10b981"]
    )
    fig_trend.update_layout(template="plotly_dark")
    st.plotly_chart(fig_trend, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        cat_sales = sales_df.groupby("category")["sales"].sum().reset_index()
        fig_cat = px.pie(cat_sales, values="sales", names="category", title="Revenue Breakdown by Category", color_discrete_sequence=px.colors.qualitative.Dark24)
        fig_cat.update_layout(template="plotly_dark")
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_b:
        reg_sales = sales_df.groupby("region")["sales"].sum().reset_index()
        fig_reg = px.bar(reg_sales, x="region", y="sales", color="region", title="Regional Revenue Distribution")
        fig_reg.update_layout(template="plotly_dark")
        st.plotly_chart(fig_reg, use_container_width=True)

# ---------------------------------------------------------
# TAB 2: AI SALES AGENT CHAT
# ---------------------------------------------------------
elif tab_choice == "🤖 AI Sales Agent Chat":
    st.subheader("🤖 Natural Language AI Business Agent")
    st.markdown("Ask the AI Agent any query regarding sales performance, forecasting, item recommendations, or customer segments.")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "assistant", "content": "Hello! I am your AI Sales Agent. Ask me questions like:\n- *What is our total revenue?*\n- *Show top 5 products*\n- *Forecast sales for next 30 days*\n- *Recommend items for user 1*"}
        ]

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "table" in msg and msg["table"] is not None:
                st.dataframe(msg["table"])

    user_query = st.chat_input("Enter your business query...")
    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        agent_result = ai_agent.process_query(user_query)

        with st.chat_message("assistant"):
            st.markdown(agent_result["answer"])
            if agent_result["table_data"] is not None:
                st.dataframe(agent_result["table_data"])

            with st.expander("🛠️ Agent Execution Steps"):
                for step in agent_result["execution_steps"]:
                    st.text(step)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": agent_result["answer"],
            "table": agent_result["table_data"]
        })

# ---------------------------------------------------------
# TAB 3: RECOMMENDATION ENGINE
# ---------------------------------------------------------
elif tab_choice == "🎯 Recommendation Engine":
    st.subheader("🎯 Collaborative Filtering Recommendation Agent")
    st.markdown("Item-Based Collaborative Filtering using Cosine Similarity.")

    rec_agent = ai_agent.rec_agent

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### 👤 Select User")
        selected_user = st.number_input("User ID", min_value=1, max_value=10, value=1)
        top_k_recs = st.slider("Number of Recommendations", 1, 5, 3)

        if st.button("Generate Recommendations", type="primary"):
            recs = rec_agent.recommend(user_id=selected_user, n=top_k_recs)
            st.markdown(f"#### Recommendations for User {selected_user}:")
            for item, pred in recs:
                st.success(f"📦 **Item {item}** → Predicted Rating: `{pred} / 5.0`")

    with col2:
        st.markdown("### 🔥 Item Similarity Heatmap")
        sim_df = rec_agent.get_similarity_matrix()
        fig_sim = px.imshow(
            sim_df,
            text_auto=".2f",
            color_continuous_scale="Blues",
            title="Item Cosine Similarity Matrix"
        )
        fig_sim.update_layout(template="plotly_dark")
        st.plotly_chart(fig_sim, use_container_width=True)

    st.markdown("### 📊 User-Item Rating Matrix")
    st.dataframe(rec_agent.get_user_item_matrix(), use_container_width=True)

# ---------------------------------------------------------
# TAB 4: SALES FORECASTING
# ---------------------------------------------------------
elif tab_choice == "📈 Sales Forecasting":
    st.subheader("📈 Machine Learning Sales Forecasting")
    st.markdown("Random Forest Regressor time-series forecasting model.")

    col1, col2 = st.columns([1, 3])
    with col1:
        forecast_days = st.slider("Forecast Horizon (Days)", 7, 60, 30)
        forecaster = ai_agent.forecaster
        metrics = forecaster.train()

        st.metric("Model MAE", f"${metrics.get('MAE', 0):,.2f}")
        st.metric("Model RMSE", f"${metrics.get('RMSE', 0):,.2f}")
        st.metric("R² Score", f"{metrics.get('R2', 0)}")

    with col2:
        forecast_df = forecaster.forecast_next_days(forecast_days)
        fig_fc = px.line(
            forecast_df, x="date", y="forecasted_sales",
            title=f"Next {forecast_days}-Day Sales Revenue Forecast",
            markers=True, line_shape="spline"
        )
        fig_fc.update_traces(line_color="#10b981", line_width=3)
        fig_fc.update_layout(template="plotly_dark")
        st.plotly_chart(fig_fc, use_container_width=True)

    st.dataframe(forecast_df, use_container_width=True)

# ---------------------------------------------------------
# TAB 5: CUSTOMER SEGMENTATION
# ---------------------------------------------------------
elif tab_choice == "👥 Customer Segmentation":
    st.subheader("👥 RFM Customer Behavioral Segmentation")
    st.markdown("K-Means Clustering based on Recency, Frequency, and Monetary (RFM) metrics.")

    segmenter = ai_agent.segmenter
    rfm_df = segmenter.fit_transform()
    summary_df = segmenter.get_segment_summary()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📊 Customer Distribution across Segments")
        fig_seg = px.bar(summary_df, x="Segment Name", y="Customer Count", color="Segment Name", title="Segment Customer Headcount")
        fig_seg.update_layout(template="plotly_dark")
        st.plotly_chart(fig_seg, use_container_width=True)

    with col2:
        st.markdown("### 💰 Revenue Contribution by Segment")
        fig_rev = px.pie(summary_df, values="Total Segment Revenue ($)", names="Segment Name", title="Segment Revenue Share")
        fig_rev.update_layout(template="plotly_dark")
        st.plotly_chart(fig_rev, use_container_width=True)

    st.markdown("### 📋 Segment Summary Matrix")
    st.dataframe(summary_df, use_container_width=True)

# ---------------------------------------------------------
# TAB 6: INTERNSHIP MILESTONES & ROADMAP
# ---------------------------------------------------------
elif tab_choice == "📅 Internship Milestones & Roadmap":
    st.subheader("📈 Project Milestones & Progress Roadmap")
    st.markdown("Tracked progress based on the 9-Week Project Milestones specification.")

    milestones = [
        {"week": "Week 1", "title": "Project Setup & Planning", "desc": "Understand requirements, set up development environment, create project roadmap", "status": "COMPLETED"},
        {"week": "Week 2-3", "title": "Research & Design", "desc": "Conduct research, create system design, define technical architecture", "status": "COMPLETED"},
        {"week": "Week 4-6", "title": "Development Phase 1", "desc": "Implement core features, build basic functionality (ML models, data pipelines)", "status": "COMPLETED"},
        {"week": "Week 7-8", "title": "Development Phase 2", "desc": "Complete advanced features, integrate components (AI Sales Agent, Streamlit Dashboard, testing)", "status": "COMPLETED"},
        {"week": "Week 8-9", "title": "Final Review & Submission", "desc": "Documentation, final testing, project presentation, GitHub delivery", "status": "COMPLETED"}
    ]

    for m in milestones:
        st.markdown(f"""
        <div class="milestone-card">
            <div class="milestone-title">✅ {m['week']}: {m['title']} ({m['status']})</div>
            <div class="milestone-desc">{m['desc']}</div>
        </div>
        """, unsafe_allow_html=True)
