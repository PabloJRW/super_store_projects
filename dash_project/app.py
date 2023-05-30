import os
import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from datetime import datetime

app = Dash(__name__, external_stylesheets=['styles.css'])

DATA_PATH = os.path.join('..','datasets','raw','Superstore.csv')
store_df = pd.read_csv(DATA_PATH, parse_dates=['Order Date', 'Ship Date'], encoding='latin-1')

app.layout = html.Div(id='main-div',children=[
    #DIV - HEADER
    html.Div(
        html.H1(id='title',
                children='Super Store Report')
    ),

    # DIV - SELECTORS
    html.Div(id='selectors-div',
             children=[
                 html.Div(id='option',
                          className='selector',
                          children=
                              dcc.RadioItems(
                                  options=['Sales','Profit','Discount','Quantity'],
                                  value='Sales',
                                  style={'display':'flex'}
                              )
                 ),

                 html.Div(id='date-range-picker',
                          className='selector',
                          children=
                              dcc.DatePickerRange(
                                  start_date=datetime(2017,1,1),
                                  end_date=datetime(2017,12,31),
                                  min_date_allowed=datetime(2016,1,1),
                                  max_date_allowed=datetime(2017,12,31)
                              )
                 ),

                 html.Div(id='option2',
                          className='selector',
                          children=
                              dcc.RadioItems(
                                  options=['Region', 'Category'],
                                  value='Region',
                                  style={'display':'flex'}
                              )
                 )

             ]
    ),
    
    # DIV - FIRST VIZ
    html.Div(  
        className='principal-graph',
        children=[
            dcc.Graph(id='1st-graph',
                      figure={'data':[go.Line(x=store_df['Order Date'].sort_values(),
                                              y=store_df['Sales'])]
                             }
                      )
        ]
    ),   
     
    # DIV - DUAL VIZ
    html.Div(
        className='div-viz',
        children = [
            html.Div(className='bi-viz',
                     children=[
                         dcc.Graph(id='2nd-graph')
                     ]
                    ),
            html.Div(className='bi-viz',
                     children=[
                         dcc.Graph(id='3rd-graph')
                     ]
                    )
        ]
    )

], style={'overflow-y':'hidden'})


@app.callback(Output('2nd-graph', 'figure'),
              [Input('option2', 'value'),
               Input('option', 'value')])
def groupingData(group_by, option23):
    """Function that group data by 'group_by' and return percentage variables"""
    
    # Grouping data by feat
    grouping = store_df.groupby(by=group_by).sum().drop('Postal Code', axis=1)
    
    fig = [go.Bar(x=grouping.index, 
                  y=grouping[option23],
                  name=group_by)]

    return fig

  
if __name__=='__main__':
    app.run_server(host='127.0.0.1', port='8050',debug=True)