import plotly.express as px
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

st.subheader("Summary")

if filtered_data.empty:
    st.warning("No data is available for the selected filters.")
else:
    latest_year = int(filtered_data["year"].max())
    latest_data = filtered_data[filtered_data["year"] == latest_year]
    top_row = latest_data.sort_values("value", ascending=False).iloc[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Latest year", latest_year)
    col2.metric("Countries/areas", filtered_data["country"].nunique())
    col3.metric("Average value", f"{latest_data['value'].mean():.2f}%")
    col4.metric("Highest country", top_row["country"])

    st.info(
        f"In {latest_year}, the highest value in the selected data was "
        f"{top_row['country']} at {top_row['value']:.2f}%."
    )

    st.subheader("Trend over time")
    line_chart = px.line(
        filtered_data,
        x="year",
        y="value",
        color="country",
        markers=True,
        title="Renewable electricity production excluding hydroelectric",
        labels={
            "year": "Year",
            "value": "Renewable electricity excluding hydroelectric (% of total)",
            "country": "Country",
        },
    )
    st.plotly_chart(line_chart, use_container_width=True)

st.subheader("Dataset preview")
st.dataframe(filtered_data.head(20), use_container_width=True)

st.write(f"Total rows loaded: {len(filtered_data)}")
st.write(
    f"Selected year range: {selected_year_range[0]} to {selected_year_range[1]}"
)
st.write(f"Total countries/areas: {filtered_data['country'].nunique()}")
