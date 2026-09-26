# 🤖 AI Agent & Machine Learning Solutions (Internship Project)

[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.64.0-ff4b4b.svg)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.9.0-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An end-to-end **AI-Powered Sales Intelligence & Recommendation System** featuring an autonomous **AI Sales Agent**, **Item-Based Collaborative Filtering**, **Sales Time-Series Forecasting**, **RFM Customer Segmentation**, and an interactive multi-tab **Streamlit Web Dashboard**.

Developed as an **Internship Submission Project** adhering to the **9-Week Project Milestones** roadmap.

🌐 **Live Demo URL**: [https://c079e599b2b71bd9-49-200-190-214.serveousercontent.com](https://c079e599b2b71bd9-49-200-190-214.serveousercontent.com)  
🐙 **GitHub Repository**: [https://github.com/abhiabhishek50518-art/AI-Agent-ML-Solutions](https://github.com/abhiabhishek50518-art/AI-Agent-ML-Solutions)


---

## 📅 Project Milestones & Execution Roadmap

This project strictly follows the 9-Week Project Milestone structure:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  ✔ Week 1: Project Setup & Planning                                                   │
│    Understand requirements, set up development environment, create project roadmap     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  ✔ Week 2-3: Research & Design                                                         │
│    Conduct research, create system design, define technical architecture               │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  ✔ Week 4-6: Development Phase 1                                                      │
│    Implement core features, build basic functionality (Collaborative Filtering, ML)   │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  ✔ Week 7-8: Development Phase 2                                                      │
│    Complete advanced features, integrate components, testing (AI Agent, Dashboard)     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│  ✔ Week 8-9: Final Review & Submission                                                 │
│    Documentation, final testing, project presentation, delivery                       │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🌟 Key Features

1. **🤖 Autonomous AI Sales Agent**: Parses natural language business queries (e.g., *"What is our total revenue?"*, *"Forecast sales for next 30 days"*), executes multi-tool workflows, and provides structured executive insights.
2. **🎯 Collaborative Filtering Recommendation Engine**: Computes Cosine Similarity across item rating vectors to predict user preferences and output top-K recommendations.
3. **📈 Random Forest Sales Forecasting**: Time-series ML model predicting revenue and product demand up to 60 days into the future with accuracy metrics ($MAE$, $RMSE$, $R^2$).
4. **👥 RFM Customer Segmentation**: Clusters customer accounts into 4 behavioral segments (*VIP Champions*, *Loyal Spenders*, *Steady Customers*, *At-Risk*) using $K$-Means clustering.
5. **📊 Interactive Streamlit Dashboard**: Dark-mode glassmorphic web dashboard with real-time financial metrics, Plotly interactive charts, chat assistant, and project milestone progress tracking.

---

## 📁 Repository Structure

```
AI-Agent-ML-Solutions/
├── data/
│   ├── sales_data.csv                 # Synthetic sales transaction dataset
│   └── user_ratings.csv               # User-Item rating matrix dataset
├── docs/
│   ├── project_overview.md            # Problem statement & business requirements
│   ├── project_roadmap.md             # 9-Week milestone execution roadmap
│   ├── system_design.md               # Technical system design & architecture
│   ├── dataset_selection.md           # Data dictionary & feature engineering docs
│   ├── internship_report.md           # Complete 9-Week Final Submission Report
│   └── milestones/                    # Weekly milestone completion documentation
│       ├── week1_setup_planning.md
│       ├── week2_3_research_design.md
│       ├── week4_6_dev_phase1.md
│       ├── week7_8_dev_phase2.md
│       └── week8_9_final_submission.md
├── reports/
│   └── AI_Agent_ML_Solutions_Presentation.md # Pitch deck presentation markdown
├── src/
│   ├── data_processing/               # Data generation & transformation pipeline
│   │   └── generate_datasets.py
│   ├── ml_models/                     # Core Machine Learning models
│   │   ├── collaborative_filtering.py # Recommendation Agent
│   │   ├── sales_forecasting.py       # Random Forest Forecaster
│   │   └── customer_segmentation.py   # RFM K-Means Clustering
│   ├── agents/                        # Autonomous AI Agent Framework
│   │   ├── query_parser.py            # Intent parser
│   │   └── ai_sales_agent.py          # Multi-tool agent engine
│   └── dashboard/                     # Streamlit multi-tab web dashboard
│       └── app.py
├── tests/                             # Pytest automated unit test suite
│   ├── test_collaborative_filtering.py
│   ├── test_sales_forecasting.py
│   └── test_ai_agent.py
├── requirements.txt                   # Project dependencies
└── README.md                          # Main project documentation
```

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/abhiabhishek50518-art/AI-Agent-ML-Solutions.git
cd AI-Agent-ML-Solutions
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate Datasets (Optional)
```bash
python src/data_processing/generate_datasets.py
```

### 4. Run the Streamlit Web Application
```bash
python -m streamlit run src/dashboard/app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Running Automated Unit Tests

Run the full pytest suite to verify model predictions, agent intent routing, and matrix computations:

```bash
python -m pytest tests/
```

---

## 💻 Tech Stack & Frameworks

- **Programming Language**: Python 3.14
- **Machine Learning & Analytics**: Pandas, NumPy, Scikit-Learn, SciPy
- **Data Visualization**: Plotly Express, Matplotlib, Seaborn
- **Web Dashboard**: Streamlit
- **Testing**: Pytest
- **Version Control**: Git & GitHub

---

## 📜 License & Author

- **Author**: Abhi Abhishek
- **GitHub**: [abhiabhishek50518-art](https://github.com/abhiabhishek50518-art)
- **Repository**: [AI-Agent-ML-Solutions](https://github.com/abhiabhishek50518-art/AI-Agent-ML-Solutions)