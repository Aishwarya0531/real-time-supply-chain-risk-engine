Project Title

Real-Time Supply Chain Risk & Oil Price Analytics Engine

🔹 Business Problem

Commodity price volatility, especially oil, directly impacts procurement costs, logistics pricing, and inflation exposure.
Most organizations react after costs rise, using static reports and lagging indicators.

This project builds a decision-ready analytics system that:

Continuously ingests oil price data

Cleans and normalizes it for analytical trust

Quantifies short-term volatility and demand risk

Surfaces insights through an executive Power BI dashboard

The goal is proactive risk visibility, not retrospective reporting.

🔹 Solution Overview

This system follows a production-style analytics architecture:

API → Raw Data → Clean Layer → Golden Analytics View → Dashboard & Forecasting

Key outcomes:

Accurate, deduplicated price history

Rolling trend and volatility metrics

Risk classification for procurement decisions

Executive-ready dashboard for monitoring instability

🔹 Architecture & Data Flow

1. Data Ingestion (Python ETL)

Live oil prices fetched from external API

Raw data stored without transformation for auditability

2. Data Cleaning & Normalization (SQL)

Duplicate handling using composite keys

Null and invalid values filtered

Idempotent inserts to support reruns

3. Analytics Layer (SQL Window Functions)

Rolling averages and volatility

Trend preservation without row collapse

Risk categorization using statistical thresholds

4. Forecasting & Driver Analysis (Python)

7-day price forecasting using historical trends

Feature importance analysis to explain drivers (trend vs volatility)

5. Visualization (Power BI)

Executive KPI cards

Trend vs volatility separation

Written business insights embedded in the dashboard

🔹 Key Metrics Delivered

Current Oil Price (USD)

Rolling 3-Period Average

Short-Term Volatility Index

Demand Risk Classification

Projected Price Trend (7 Days)

🔹 Tools & Technologies

Python: API ingestion, forecasting

PostgreSQL: Data storage, analytics views

SQL: Window functions, constraints, normalization

Power BI: Executive dashboard & storytelling

Git/GitHub: Version control

🔹 Why This Project Stands Out

Designed as a business solution, not a model demo

Uses SQL for analytics where it belongs

Avoids black-box ML in favor of explainable insights

Mirrors real enterprise data workflows

Emphasizes decision-making, not just charts

🔹 Potential Extensions

Automated alerts when volatility crosses thresholds

Integration with logistics or inflation indicators

Scheduled refresh & cloud deployment
## Executive Dashboard Preview

![Supply Chain Risk Dashboard](assets/dashboard_scre.png)
