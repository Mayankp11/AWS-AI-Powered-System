#🚀 AI-Powered AWS Cost Intelligence System
📌 Overview

This project is an AI-assisted AWS cost analysis and monitoring pipeline built using Python and Google Gemini API.

It processes AWS billing CSV reports, performs multi-dimensional cost analysis, detects anomalies, and generates automated FinOps insights using AI.

The goal is to convert raw billing data into actionable business intelligence.

🧠 Problem Statement

AWS billing reports are complex and difficult to interpret manually. Organizations need:

Clear cost breakdown by service and account

Detection of unusual cost spikes

Optimization recommendations

Executive-friendly reporting

This project automates that workflow.

⚙️ Tech Stack

Python

Pandas

Matplotlib

Google Gemini API

Jupyter Notebook

📂 Dataset

Input: AWS Monthly Billing CSV

Columns include:

UsageDate

Service

LinkedAccount

Region

UsageType

UsageQuantity

UnblendedCost

🔍 Project Workflow
1️⃣ Data Ingestion

Loaded AWS billing CSV into Pandas DataFrame.

df = pd.read_csv(file_path)

2️⃣ Data Cleaning

Converted date column to datetime

Converted cost column to numeric

Removed invalid rows

df['UsageDate'] = pd.to_datetime(df['UsageDate'], dayfirst=True)
df['UnblendedCost'] = pd.to_numeric(df['UnblendedCost'], errors='coerce')
df = df.dropna(subset=['UnblendedCost'])

3️⃣ Cost Analysis (Multi-Dimensional)

✔ Cost by Service
✔ Cost by Linked Account
✔ Cost by Region
✔ Cost by Usage Type
✔ Daily Cost Trend

Example:

service_summary = df.groupby("Service")["UnblendedCost"].sum()

4️⃣ Anomaly Detection

Implemented statistical anomaly detection to identify abnormal cost spikes in daily trends.

This enables proactive FinOps monitoring.

5️⃣ AI Integration (Gemini API)

Converted structured cost summaries into AI-generated insights.

Example:

prompt = f"""
Analyze AWS cost breakdown and provide:
1. Top cost drivers
2. Optimization strategies
3. Governance recommendations
"""


Gemini generated:

Root cause explanations

Cost optimization strategies

Executive-level summaries

6️⃣ Visualization

Created management-friendly visualizations:

Bar charts for cost by service

Bar charts for cost by account

Daily trend graphs

These provide quick executive visibility.

📊 Key Insights Generated

Identified top cost-driving services

Detected unusual daily cost spikes

Highlighted expensive regions

Suggested reserved instance and savings plan strategies

Recommended governance and tagging improvements

🎯 Business Impact

This solution:

Reduces manual billing analysis effort

Improves cost transparency

Enables proactive anomaly detection

Automates FinOps recommendations using AI

Provides executive-ready insights

🚀 How to Run

Clone repository

Create virtual environment

python -m venv gemini_env
gemini_env\Scripts\activate


Install dependencies

pip install pandas matplotlib google-generativeai jupyter


Add Gemini API key

genai.configure(api_key="YOUR_API_KEY")


Run notebook

jupyter notebook

🧠 What I Learned

Handling real-world billing data inconsistencies

Time-series cost analysis

Statistical anomaly detection

AI API integration for automated insights

FinOps cost governance principles

Building reproducible data workflows

📌 Future Improvements

Cost forecasting using ML

Automated alert system

Executive PDF report generation

Streamlit dashboard

Integration with Slack/Email notifications
