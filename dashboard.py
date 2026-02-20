# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

# --- Read DB credentials from Streamlit Secrets ---
DB_USER = st.secrets["DB_USER"]
DB_PASSWORD = st.secrets["DB_PASSWORD"]
DB_HOST = st.secrets["DB_HOST"]
DB_PORT = st.secrets["DB_PORT"]   # string is fine
DB_NAME = st.secrets["DB_NAME"]


engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)

# --- Streamlit title ---
st.title("AWS Billing Dashboard 💰")

# --- Total rows and total cost ---
with engine.connect() as conn:
    total_rows = conn.execute(text('SELECT COUNT(*) FROM billing_data;')).scalar()
    total_cost = conn.execute(text('SELECT SUM("UnblendedCost") FROM billing_data;')).scalar()

st.metric("Total Rows", total_rows)
st.metric("Total Cost ($)", round(total_cost, 2))

# --- Top 5 services ---
query_top_services = """
SELECT "Service", SUM("UnblendedCost") AS total_cost
FROM billing_data
GROUP BY "Service"
ORDER BY total_cost DESC
LIMIT 5;
"""
top_services_df = pd.read_sql(query_top_services, engine)

fig_services = px.bar(
    top_services_df,
    x="Service",
    y="total_cost",
    title="Top 5 Services by Total Cost",
    labels={"total_cost": "Total Cost ($)"}
)
st.plotly_chart(fig_services)
