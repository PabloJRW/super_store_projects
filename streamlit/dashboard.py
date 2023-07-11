import os
import datetime
import pandas as pd
import streamlit as st

pd.set_option('display.float_format','{:.2f}'.format)
DATA_PATH = os.path.join('datasets','raw','Superstore.csv')
data = pd.read_csv(DATA_PATH, parse_dates=['Order Date', 'Ship Date'], encoding='latin-1')
data_by_region = data.groupby('Region')[['Sales', 'Profit']].sum()
data_by_segment = data.groupby('Segment')[['Sales', 'Profit']].sum()


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


st.line_chart(data=data, x='Order Date', y='Sales')

col1, col2 = st.columns(2)

with col1:
    st.subheader("By Region")
    st.bar_chart(data_by_region[options])

with col2:
    st.subheader("By Segment")
    st.bar_chart(data_by_segment[options])
