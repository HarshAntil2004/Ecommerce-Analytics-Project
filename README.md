# RetailPulse Analytics — End-to-End Data Analyst Portfolio Project

A complete, realistic analytics case study: raw messy e-commerce order data →
cleaned data → SQL analysis → EDA → business insights. Built as a portfolio
project for entry-level Data Analyst / Business Analyst roles.

## 1. Business Background

RetailPulse is a fictional mid-size Indian online retailer selling across six
categories (Electronics, Fashion, Home & Kitchen, Beauty, Sports, Grocery).
Leadership wants a Data Analyst to explain what's driving revenue, which
customers/products matter most, and where to focus retention and marketing spend.

**Problem Statement:** Order, customer, and product data currently sits in
disconnected, messy exports. There is no single source of truth for revenue
trends, customer value, or product performance.

**Business Goals**
- Understand revenue trends and seasonality
- Identify top customers, products, and regions
- Quantify the impact of discounts, cancellations, and returns
- Provide leadership a dashboard for ongoing monitoring

**Key KPIs:** Net Revenue, Average Order Value, Repeat Customer Rate, Return
Rate, Revenue by Category/Region, Customer Lifetime Value.

**Stakeholders:** Head of E-commerce, Marketing Lead, Regional Sales Managers,
Customer Experience team.

## 2. Dataset

Synthetic but realistic, generated with `python/generate_dataset.py`:
- 12,000+ rows after cleaning, 25+ raw columns
- Mixed data types: dates, categoricals, numerics, booleans
- Deliberately messy: duplicates, missing values, inconsistent casing,
  mixed date formats, currency-formatted numeric strings, outliers,
  impossible values (negative age/cost)

## 3. Project Structure

```
retailpulse-analytics/
├── data/
│   ├── raw/                # generated messy raw data
│   └── cleaned/            # cleaned, analysis-ready data
├── python/
│   ├── generate_dataset.py # synthetic data generator
│   ├── clean_data.py       # cleaning + feature engineering
│   ├── load_to_mysql.py    # loads cleaned data into MySQL
│   └── eda.py              # exploratory data analysis + charts
├── sql/
│   ├── 01_create_schema.sql
│   └── 03_analysis_queries.sql   # 12 business SQL queries
├── automation/
│   └── main.py              # single-command pipeline runner
├── tableau/                 # (add .twbx workbook here)
├── dashboard_images/         # dashboard screenshots
├── reports/                  # EDA chart outputs
├── docs/                     # documentation
├── logs/                     # pipeline run logs
├── requirements.txt
└── README.md
```

## 4. How to Run

```bash
pip install -r requirements.txt

# Run the whole pipeline (generation -> cleaning -> EDA)
cd automation
python main.py --skip-mysql

# To also load into MySQL, first run sql/01_create_schema.sql against your
# MySQL server, set RP_DB_HOST / RP_DB_USER / RP_DB_PASSWORD, then:
python main.py
```

## 5. Business Insights (sample — see docs/business_insights.md for full list)

- Electronics contributes the largest share of net revenue despite lower order counts, due to high average order value.
- Cancelled + Returned orders make up roughly 16% of all orders — a meaningful revenue leakage point.
- A small share of customers (the "Champion" RFM segment) account for a disproportionate share of lifetime revenue.
- Discount usage varies significantly by category and correlates with order volume more than with net revenue growth.

## 6. Tech Stack

Python (Pandas, NumPy, Matplotlib, Seaborn), MySQL, SQL (window functions,
CTEs, views), Tableau, Git/GitHub.

## 7. Documentation

See `/docs` for: ER diagram description, workflow diagram description,
resume bullet points, and interview preparation Q&A.

## 8. Future Improvements

- Add a real Tableau `.twbx` workbook with executive/sales/customer dashboards
- Add Airflow-based scheduling for the pipeline
- Add unit tests (pytest) for cleaning functions
- Add a Streamlit app for interactive exploration
