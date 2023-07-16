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


st.set_page_config(page_title="SuperStore")

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

# Line chart view mode
checkbox_value = st.sidebar.checkbox("Line Chart View", value=True)

#  #######################################################################################

filtered_by_year = data[(data.index.year >= min_year_selected) & (data.index.year <= max_year_selected)]

data_by_region = filtered_by_year.groupby('Region')[['Sales', 'Profit']].sum()
data_by_segment = filtered_by_year.groupby('Segment')[['Sales', 'Profit']].sum()

resample_data = filtered_by_year.resample('M').sum()

# DASHBOARD ############################################################################################


months_labels = ['January','February','March','April','May','June','July','August','September','October','November','December']

# Line chart +++++++++++++

if checkbox_value:

    fig = go.Figure()
    for year in range(min_year_selected, max_year_selected+1):
        fig.add_trace(go.Scatter(y=resample_data[resample_data.index.year == year][options],
                                 mode='lines',
                                 name=year))

    fig.update_layout(title=f"{options} by year",
                      xaxis_title="Month",
                      yaxis_title=f"$ {options}",
                      legend_title="Legend Title",
                      xaxis=dict(
                          tickvals=[1,2,3,4,5,6,7,8,9,10,11,12],
                          ticktext=months_labels
                        )
                  
    )
    st.plotly_chart(fig)

else:
    for year in range(min_year_selected, max_year_selected+1):
        fig = go.Figure(go.Scatter(y=resample_data[(resample_data.index.year >= min_year_selected) & (resample_data.index.year <= max_year_selected)][options],
                             mode='lines'
                            ))
        
        fig.update_layout(title=f"{options} by year",
                      xaxis_title="Month",
                      yaxis_title=f"$ {options}",
                      legend_title="Legend Title",
                        )
                  


    st.plotly_chart(fig)
        

col1, col2 = st.columns(2)

fig_by_region = go.Figure(go.Bar(x=data_by_region.index, y=data_by_region[options]))
with col1:
    st.subheader(f"{options} by Region")
    st.plotly_chart(fig_by_region, use_container_width=True)
    

fig_by_segment = go.Figure(go.Bar(x=data_by_segment.index, y=data_by_segment[options]))
with col2:
    st.subheader(f"{options} by Segment")
    st.plotly_chart(fig_by_segment, use_container_width=True)

