import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DUMMY_DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DUMMY_DB_NAME")
TABLE_NAME = os.getenv("RDS_TABLE_NAME")

# -----------------------------
# Create Database Engine
# -----------------------------
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(page_title="Dummy Dashboard", layout="wide")
st.title("📊 Dummy RDS Dashboard")

# -----------------------------
# Fetch Data from RDS
# -----------------------------
@st.cache_data
def load_data():
    query = f"SELECT * FROM {TABLE_NAME}"
    return pd.read_sql(query, engine)

try:
    df = load_data()
    st.success("Connected to RDS ✅")

    # Show basic metrics
    col1, col2 = st.columns(2)
    col1.metric("Total Rows", len(df))
    col2.metric("Total Columns", len(df.columns))

    st.divider()

    st.subheader("Preview Data")
    st.dataframe(df)

except Exception as e:
    st.error("Connection Failed ❌")
    st.error(e)