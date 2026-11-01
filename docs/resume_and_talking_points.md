# Resume, LinkedIn & Interview Talking Points

## Resume Bullet Points (ATS-friendly)

- Built an end-to-end e-commerce analytics pipeline in Python and MySQL, processing 12,000+ orders across 25+ raw attributes, improving data reliability by resolving duplicates, missing values, and format inconsistencies.
- Designed a normalized MySQL schema (customers/orders) with primary/foreign keys and indexes; wrote 12 advanced SQL queries using CTEs, window functions, and RFM segmentation to surface customer lifetime value and retention patterns.
- Performed exploratory data analysis using Pandas, Matplotlib, and Seaborn to identify revenue drivers, seasonality, and return-rate issues, translating findings into actionable business recommendations.
- Automated the full data pipeline (ingestion → cleaning → validation → MySQL load → reporting) with a single-command Python script using logging and modular functions.
- Delivered 15+ data-backed business insights and recommendations covering revenue concentration, customer segmentation, and operational return-rate leakage.

## GitHub Repository Description

> End-to-end data analytics project simulating a mid-size e-commerce retailer.
> Covers data generation, cleaning, MySQL schema design, advanced SQL analysis
> (CTEs, window functions, RFM), EDA, and business insight generation — built
> to demonstrate the full Data Analyst workflow from raw data to decision-making.

## LinkedIn Project Description

> I built RetailPulse Analytics, an end-to-end data analytics project simulating
> a real e-commerce company's order data. The project takes messy, realistic
> raw data through cleaning, MySQL database design, advanced SQL analysis
> (window functions, CTEs, RFM segmentation), exploratory data analysis in
> Python, and finishes with concrete, actionable business recommendations.
> It's designed to mirror the actual workflow of a Data Analyst — not just a
> notebook of charts, but a reproducible pipeline with a real business
> narrative behind every decision.

## Interview Talking Points

- **Why this project?** I wanted a project that covered the full lifecycle —
  not just a Kaggle notebook — including database design and an automated
  pipeline, since that's closer to how analytics work actually happens in a company.
- **Biggest technical challenge:** Handling inconsistent date formats and
  currency-formatted strings inside a numeric column without silently
  corrupting values — solved with regex-based parsing and validation asserts
  before saving cleaned data.
- **A business decision this project could inform:** The RFM segmentation
  identifies "Champion" customers who could be prioritized for a loyalty
  program, and quantifies the return-rate leakage operations should target first.
- **What I'd do differently at scale:** Move from CSV batch processing to
  incremental/streaming ingestion, add orchestration (Airflow), and add
  automated data-quality tests (Great Expectations or pytest-based checks).
