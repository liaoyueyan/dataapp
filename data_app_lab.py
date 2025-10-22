import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import matplotlib.pyplot as plt

st.title("California Housing Data (1990) by [Your Name]")

# Load Data
@st.cache_data
def load_data():
    url = "housing.csv"  # replace with your dataset path
    data = pd.read_csv(url)
    data = data.dropna()
    return data

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
house_price = st.sidebar.slider("Minimal Median House Price", 
                                int(df.median_house_value.min()), 
                                int(df.median_house_value.max()), 
                                200000)

# Filter by price
filtered_df = df[df.median_house_value >= house_price]

# Sidebar: Location type (optional example based on ocean proximity)
location_types = st.sidebar.multiselect(
    "Choose the location type",
    options=df.ocean_proximity.unique(),
    default=df.ocean_proximity.unique()
)

filtered_df = filtered_df[filtered_df.ocean_proximity.isin(location_types)]

# Sidebar: Income filter
income_level = st.sidebar.radio(
    "Choose income level",
    ('Low (≤ 2.5)', 'Medium (> 2.5 & ≤ 4.5)', 'High (> 4.5)')
)

if income_level == 'Low (≤ 2.5)':
    filtered_df = filtered_df[filtered_df.median_income <= 2.5]
elif income_level == 'Medium (> 2.5 & ≤ 4.5)':
    filtered_df = filtered_df[(filtered_df.median_income > 2.5) & (filtered_df.median_income <= 4.5)]
else:
    filtered_df = filtered_df[filtered_df.median_income > 4.5]

st.subheader("See more filters in the sidebar:")

# Map Visualization
st.map(filtered_df[['latitude', 'longitude']])

# Histogram
st.subheader("Histogram of Median House Values")
fig, ax = plt.subplots()
ax.hist(filtered_df.median_house_value, bins=30)
st.pyplot(fig)