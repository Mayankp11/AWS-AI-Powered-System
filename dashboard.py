import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

# ✅ BETTER: Cache the database connection - reuse across reruns
@st.cache_resource
def get_db_connection():
    """Create and cache database connection"""
    return create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
        pool_size=5,
        max_overflow=10,
        pool_recycle=3600,
        pool_pre_ping=True  # Test connection before using
    )

# ✅ BETTER: Cache expensive database queries (1 hour TTL)
@st.cache_data(ttl=3600)
def get_total_metrics():
    """Get total rows and cost"""
    engine = get_db_connection()
    with engine.connect() as conn:
        total_rows = conn.execute(text('SELECT COUNT(*) FROM billing_data;')).scalar()
        total_cost = conn.execute(text('SELECT SUM("UnblendedCost") FROM billing_data;')).scalar()
    return total_rows, total_cost

@st.cache_data(ttl=3600)
def get_top_services():
    """Get top 10 services"""
    engine = get_db_connection()
    query = """
    SELECT "Service", SUM("UnblendedCost") AS total_cost
    FROM billing_data
    GROUP BY "Service"
    ORDER BY total_cost DESC
    LIMIT 10;
    """
    return pd.read_sql(query, engine)

@st.cache_data(ttl=3600)
def get_daily_trend():
    """Get daily cost trend"""
    engine = get_db_connection()
    query = """
    SELECT "UsageDate", SUM("UnblendedCost") AS daily_cost
    FROM billing_data
    GROUP BY "UsageDate"
    ORDER BY "UsageDate"
    LIMIT 90;
    """
    return pd.read_sql(query, engine)

@st.cache_data(ttl=3600)
def get_cost_by_region():
    """Get cost by region"""
    engine = get_db_connection()
    query = """
    SELECT "Region", SUM("UnblendedCost") AS total_cost
    FROM billing_data
    GROUP BY "Region"
    ORDER BY total_cost DESC
    LIMIT 10;
    """
    return pd.read_sql(query, engine)

st.set_page_config(page_title="AWS Billing Dashboard", layout="wide")
st.title("📊 AWS Billing Dashboard")

try:
    # KPIs
    total_rows, total_cost = get_total_metrics()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rows", f"{total_rows:,}")
    with col2:
        st.metric("Total Cost", f"${total_cost:,.2f}")
    with col3:
        st.metric("Status", "✅ Connected")
    
    st.divider()
    
    # Top Services
    st.subheading("Top 10 Services by Cost")
    df_services = get_top_services()
    fig_services = px.bar(
        df_services,
        x="Service",
        y="total_cost",
        color="total_cost",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_services, use_container_width=True)
    
    # Daily Trend
    st.subheading("Daily Cost Trend (Last 90 Days)")
    df_daily = get_daily_trend()
    df_daily['UsageDate'] = pd.to_datetime(df_daily['UsageDate'])
    fig_daily = px.line(df_daily, x="UsageDate", y="daily_cost", markers=True)
    st.plotly_chart(fig_daily, use_container_width=True)
    
    # Cost by Region
    st.subheading("Cost by Region")
    df_region = get_cost_by_region()
    fig_region = px.pie(df_region, names="Region", values="total_cost")
    st.plotly_chart(fig_region, use_container_width=True)
    
    st.divider()
    st.dataframe(df_services, use_container_width=True)

except Exception as e:
    st.error(f"❌ Connection Error: {str(e)}")
    st.warning("""
    **Fix RDS Connection:**
    1. AWS Console → RDS → Databases
    2. Check `aws-cost-analytics-db` is "Available"
    3. Security Groups → Inbound Rules
    4. Add: Type=PostgreSQL, Port=5432, Source=Your IP
    5. Wait 1-2 min and refresh
    """)
