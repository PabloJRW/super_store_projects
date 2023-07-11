import os
import datetime
import pandas as pd
import streamlit as st

pd.set_option('display.float_format','{:.2f}'.format)
DATA_PATH = os.path.join('datasets','raw','Superstore.csv')
data = pd.read_csv(DATA_PATH, parse_dates=['Order Date', 'Ship Date'], encoding='latin-1')
data_by_region = data.groupby('Region')[['Sales', 'Profit']].mean()


st.title("SuperStore Sales Dashboard")

st.sidebar.title("Select Options:")
options = st.sidebar.radio(
    'What are your favorite colors',
    options=['Sales', 'Profit'])

min_date = st.sidebar.date_input(
    "Select Date Range",
    datetime.date(2019, 7, 6))

max_date = st.sidebar.date_input(
    "Select Date Range",
    datetime.date(2021, 7, 6))


st.subheader("By Region")
st.bar_chart(data_by_region[options])
