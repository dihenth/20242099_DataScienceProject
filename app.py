import streamlit as st
from src.data import load_indicator_data

st.set_page_config(page_title="Renewable Electricity Dashboard", layout="wide")

st.title("Renewable Electricity Dashboard")
st.write(
    "This dashboard analyses the World Bank indicator for electricity "
    "production from renewable sources, excluding hydroelectric."
)

data = load_indicator_data()

st.subheader("Dataset preview")
st.dataframe(data.head(20), use_container_width=True)

st.write(f"Total rows loaded: {len(data)}")
st.write(f"Year range: {data['year'].min()} to {data['year'].max()}")
st.write(f"Total countries/areas: {data['country'].nunique()}")
