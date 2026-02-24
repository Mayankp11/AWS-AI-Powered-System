# ==============================
# 📦 IMPORTS
# ==============================
# Streamlit → Web app framework
import streamlit as st

# Pandas → Data manipulation
import pandas as pd

# Plotly → Interactive charts
import plotly.express as px

# SQLAlchemy → Database connection management
from sqlalchemy import create_engine, text

# dotenv → Load environment variables from .env file
from dotenv import load_dotenv

# os → Access environment variables
import os


# ==============================
# 🔐 LOAD ENVIRONMENT VARIABLES
# ==============================
# Loads DB_USER, DB_PASSWORD, DB_HOST, etc. from your .env file
load_dotenv()


# ==============================
# ⚙️ PAGE CONFIGURATION
# ==============================
st.set_page_config(
    page_title="AWS Billing Dashboard",
    layout="wide"
)

st.title("📊 AWS Billing Dashboard")


# ==============================
# 🗄 DATABASE CONNECTION (CACHED)
# ==============================
# st.cache_resource → Keeps the database connection alive
# so Streamlit doesn't recreate it on every rerun.
@st.cache_resource
def get_db_connection():
    """
    Create and cache the database connection.

    Why caching?
    - Creating DB connections is expensive.
    - Streamlit reruns the script often.
    - This ensures reuse of the same connection pool.
    """
    return create_engine(
        f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
        pool_size=5,          # Maintain up to 5 persistent connections
        max_overflow=10,      # Allow 10 temporary overflow connections
        pool_recycle=3600,    # Recycle connections every hour
        pool_pre_ping=True    # Check connection health before using
    )


# ==============================
# 📊 DATABASE QUERY FUNCTIONS (CACHED)
# ==============================
# st.cache_data → Caches expensive query results
# ttl=3600 → Refresh every 1 hour

@st.cache_data(ttl=3600)
def get_total_metrics():
    """
    Returns:
        total_rows → Total records in billing_data
        total_cost → Sum of all UnblendedCost
    """
    engine = get_db_connection()
    with engine.connect() as conn:
        total_rows = conn.execute(
            text('SELECT COUNT(*) FROM billing_data;')
        ).scalar()

        total_cost = conn.execute(
            text('SELECT SUM("UnblendedCost") FROM billing_data;')
        ).scalar()

    return total_rows, total_cost or 0


@st.cache_data(ttl=3600)
def get_top_services():
    """Return top 10 AWS services by cost."""
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
    """Return last 90 days of daily cost."""
    engine = get_db_connection()

    query = """
    SELECT "UsageDate", SUM("UnblendedCost") AS daily_cost
    FROM billing_data
    GROUP BY "UsageDate"
    ORDER BY "UsageDate"
    LIMIT 90;
    """

    df = pd.read_sql(query, engine)

    # Ensure date column is properly formatted
    df["UsageDate"] = pd.to_datetime(df["UsageDate"])

    return df


@st.cache_data(ttl=3600)
def get_cost_by_region():
    """Return top 10 regions by cost."""
    engine = get_db_connection()

    query = """
    SELECT "Region", SUM("UnblendedCost") AS total_cost
    FROM billing_data
    GROUP BY "Region"
    ORDER BY total_cost DESC
    LIMIT 10;
    """

    return pd.read_sql(query, engine)


# ==============================
# 🚀 MAIN DASHBOARD LOGIC
# ==============================
try:
    # --------------------------------
    # 📌 KPI SECTION (Top Metrics)
    # --------------------------------
    total_rows, total_cost = get_total_metrics()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Rows", f"{total_rows:,}")

    with col2:
        st.metric("Total Cost", f"${total_cost:,.2f}")

    with col3:
        st.metric("Status", "✅ Connected")

    st.divider()

    # --------------------------------
    # 📄 Raw Data Preview
    # --------------------------------
    st.subheader("📄 Raw Data Preview (First 5 Rows)")

    engine = get_db_connection()
    with engine.connect() as conn:
        preview_df = pd.read_sql(
            text("SELECT * FROM billing_data LIMIT 5"),
            conn
        )

    st.dataframe(preview_df, use_container_width=True)

    # --------------------------------
    # 📥 Fetch Chart Data
    # --------------------------------
    df_services = get_top_services()
    df_daily = get_daily_trend()
    df_region = get_cost_by_region()

    # --------------------------------
    # 📈 Daily Trend Chart (Full Width)
    # --------------------------------
    st.subheader("📈 Daily Cost Trend (Last 90 Days)")

    fig_daily = px.line(
        df_daily,
        x="UsageDate",
        y="daily_cost",
        labels={
            "daily_cost": "Cost ($)",
            "UsageDate": "Date"
        },
        template="plotly_white"
    )

    st.plotly_chart(fig_daily, use_container_width=True)

    # --------------------------------
    # 📊 Services + Regions (2 Columns)
    # --------------------------------
    col_left, col_right = st.columns(2)

    # Top Services (Bar Chart)
    with col_left:
        st.subheader("🏢 Top 10 Services")

        fig_services = px.bar(
            df_services,
            x="total_cost",
            y="Service",
            orientation="h",
            color="total_cost",
            color_continuous_scale="Reds"
        )

        st.plotly_chart(fig_services, use_container_width=True)

    # Cost by Region (Donut Chart)
    with col_right:
        st.subheader("🌍 Cost by Region")

        fig_region = px.pie(
            df_region,
            values="total_cost",
            names="Region",
            hole=0.4,  # Makes it a donut chart
            color_discrete_sequence=px.colors.sequential.RdBu
        )

        st.plotly_chart(fig_region, use_container_width=True)


# ==============================
# ❌ ERROR HANDLING
# ==============================
except Exception as e:
    st.error(f"❌ Connection Error: {str(e)}")

    st.warning("""
    **Fix RDS Connection:**
    1. AWS Console → RDS → Databases  
    2. Ensure your database is "Available"  
    3. Open Security Groups → Inbound Rules  
    4. Add: Type=PostgreSQL, Port=5432, Source=Your IP  
    5. Wait 1–2 minutes and refresh  
    """)