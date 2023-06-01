import os
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from datetime import datetime

app = Dash(__name__, external_stylesheets=['styles.css'])

DATA_PATH = os.path.join('..','datasets','raw','Superstore.csv')
store_df = pd.read_csv(DATA_PATH, parse_dates=['Order Date', 'Ship Date'], encoding='latin-1')
min_date = store_df['Order Date'].min()
max_date = store_df['Order Date'].max()


app.layout = html.Div(id='main-div',children=[
    #DIV - HEADER
    html.Div(
        html.H1(id='title',
                children='Super Store Report')
    ),

    # DIV - SELECTORS
    html.Div(id='div-selectors',
             children=[
                 html.Div(
                     className='selector',
                     children=[
                         html.H3(className='h3-selector', children='Select an option:'),
                         dcc.RadioItems(
                             id='picoloco',
                             options=['Sales','Profit','Discount','Quantity'],
                             value='Sales',
                             style={'display':'flex',
                                    'justifyContent':'space-evenly'}
                         )
                     ]
                 ),

                 html.Div(
                          className='selector',
                          children=[
                              html.H3(className='h3-selector',
                                      children='Select an option:'),
                              dcc.RadioItems(
                                  id='culosucio',
                                  options=['Region', 'Segment', 'Category', 'Sub-Category'],
                                  value='Region',
                                  style={'display':'flex'}
                              )
                          ]
                 ),

                 html.Div(
                          className='selector',
                          children=[
                              html.H3(className='h3-selector',
                                      children='Select a date range'),
                              dcc.DatePickerRange(
                                  id='date-range-picker',
                                  start_date=min_date,
                                  end_date=max_date,
                                  min_date_allowed=min_date,
                                  max_date_allowed=max_date,
                                  style={'height':'60%'}
                              )
                            ]
                 ),
             ]
    ), # DIV SELECTORS FINAL
    
    html.Div(id='div-graphs',
             children=[
                    # DIV - FIRST VIZ
                    html.Div(  
                        className='principal-graph',
                        children=[
                            dcc.Graph(id='1st-graph',
                                     figure={'data':[px.line(x=store_df['Order Date'].sort_values(),
                                                             y=store_df['Sales'])]
                                            }
                            )
                        ]
                    ),
             ])

], style={'overflow-y':'hidden'})


@app.callback(Output('1st-graph', 'figure'),
              [Input('culosucio', 'value'),
               Input('picoloco', 'value'),
               Input('date-range-picker', 'start_date'),
               Input('date-range-picker', 'end_date')])
def groupingData(group_by, option23, start_date, end_date):
    """Function that group data by 'group_by' and return percentage variables"""
    
    store_df.sort_values(by='Order Date', inplace=True)
    #Select date range
    date_range_df = store_df[(store_df['Order Date']>=start_date)&(store_df['Order Date']<=end_date)]
    # Grouping data by feat
    grouping = date_range_df.groupby(by=group_by).sum().drop('Postal Code', axis=1)
    
    fig = px.bar(x=grouping.index, 
                  y=grouping[option23])
    
    fig.update_layout(
        title={'text':"{} BY {}".format(option23.upper(), group_by.upper()),
               'x':0.5},
        xaxis_title="{}".format(group_by),
        yaxis_title="{}".format(option23)
    )

    return fig

  
if __name__=='__main__':
    app.run_server(host='127.0.0.1', port='8050',debug=True)