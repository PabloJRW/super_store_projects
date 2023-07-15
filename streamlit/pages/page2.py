import streamlit as st


st.title("Página 2")





import os
from datetime import datetime
import pandas as pd
import plotly.graph_objs as go
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
    'Select:',
    options=['Sales', 'Profit'])


# Years options
list_of_years = ((data.index.year).unique()).sort_values()

min_year_selected, max_year_selected = st.sidebar.select_slider(
    'Select a range of years',
    options=list_of_years,
    value=(list_of_years.min(), list_of_years.max()))


#  #######################################################################################

filtered_by_year = data[(data.index.year >= min_year_selected) & (data.index.year <= max_year_selected)]

data_by_region = filtered_by_year.groupby('Region')[['Sales', 'Profit']].sum()
data_by_segment = filtered_by_year.groupby('Segment')[['Sales', 'Profit']].sum()

resample_data = filtered_by_year.resample('M').sum()



fig = go.Figure()
year=[2016, 2017]
for ye in year:
    fig.add_trace(go.Scatter(y=resample_data[resample_data.index.year == ye][options],
    mode='lines',
    name=f"options {ye}"))


st.plotly_chart(fig)