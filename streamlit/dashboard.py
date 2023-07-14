import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

pd.set_option('display.float_format','{:.2f}'.format)
DATA_PATH = os.path.join('datasets','raw','Superstore.csv')
data = pd.read_csv(DATA_PATH, parse_dates=['Order Date', 'Ship Date'], encoding='latin-1')
data['Order Date'] = pd.to_datetime(data['Order Date'])
data.set_index('Order Date', inplace=True)


# Title of dashboard
st.title("SuperStore Sales Dashboard")


# SIDEBAR #########################################################################################

# Options
st.sidebar.title("Select Options:")
options = st.sidebar.radio(
    'What are your favorite colors',
    options=['Sales', 'Profit'])


# Years options
list_of_years = (data.index.year).unique()
year_selected = st.sidebar.multiselect(label="Select years:", options=list_of_years, default=[2016])


#  #######################################################################################

filtered_by_year = data.loc[data.index.year.isin(year_selected)]

data_by_region = filtered_by_year.groupby('Region')[['Sales', 'Profit']].sum()
data_by_segment = filtered_by_year.groupby('Segment')[['Sales', 'Profit']].sum()

resample_data = filtered_by_year.resample('M').sum()

# DASHBOARD ############################################################################################

for year in year_selected:
    st.line_chart(resample_data[resample_data.index.year==year]['Sales'])



col1, col2 = st.columns(2)


with col1:
    st.subheader(f"{options} by Region")
    st.bar_chart(data_by_region[options])

with col2:
    st.subheader(f"{options} by Segment")
    st.bar_chart(data_by_segment[options])
