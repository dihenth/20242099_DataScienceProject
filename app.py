import streamlit as st
from src.data import load_indicator_data

st.set_page_config(page_title="Renewable Electricity Dashboard", layout="wide")

st.title("Renewable Electricity Dashboard")
st.write(
    "This dashboard analyses the World Bank indicator for electricity "
    "production from renewable sources, excluding hydroelectric."
)

data = load_indicator_data()

min_year = int(data["year"].min())
max_year = int(data["year"].max())

selected_year_range = st.sidebar.slider(
    "Select year range",
    min_value=min_year,
    max_value=max_year,
    value=(max_year - 10, max_year),
)

countries = sorted(data["country"].unique().tolist())
selected_countries = st.sidebar.multiselect(
    "Select countries",
    options=countries,
    default=[],
)

filtered_data = data[
    (data["year"] >= selected_year_range[0]) &
    (data["year"] <= selected_year_range[1])
]

if selected_countries:
    filtered_data = filtered_data[filtered_data["country"].isin(selected_countries)]

st.subheader("Dataset preview")
st.dataframe(filtered_data.head(20), use_container_width=True)

st.write(f"Total rows loaded: {len(filtered_data)}")
st.write(
    f"Selected year range: {selected_year_range[0]} to {selected_year_range[1]}"
)
st.write(f"Total countries/areas: {filtered_data['country'].nunique()}")
