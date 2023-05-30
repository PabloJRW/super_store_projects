import os
import pandas as pd
import plotly.express as px
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

                 html.Div(id='date-range-picker',
                          className='selector',
                          children=[
                              html.H3(className='h3-selector'),
                              dcc.DatePickerRange(
                                  start_date=datetime(2017,1,1),
                                  end_date=datetime(2017,12,31),
                                  min_date_allowed=datetime(2016,1,1),
                                  max_date_allowed=datetime(2017,12,31),
                                  style={'height':'60%'}
                              )
                            ]
                 ),

                 html.Div(
                          className='selector',
                          children=
                              dcc.RadioItems(
                                  id='culosucio',
                                  options=['Region', 'Category', 'Sub-Category'],
                                  value='Region',
                                  style={'display':'flex'}
                              )
                 )

             ]
    ),
    
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
             ])

], style={'overflow-y':'hidden'})


@app.callback(Output('2nd-graph', 'figure'),
              [Input('culosucio', 'value'),
               Input('picoloco', 'value')])
def groupingData(group_by, option23):
    """Function that group data by 'group_by' and return percentage variables"""
    
    # Grouping data by feat
    grouping = store_df.groupby(by=group_by).sum().drop('Postal Code', axis=1)
    
    fig = px.bar(x=grouping.index, 
                  y=grouping[option23])
    
    fig.update_layout(
        title="{} by {}".format(option23, group_by),
        xaxis_title="{}".format(group_by),
        yaxis_title="{}".format(option23)
    )

    return fig

  
if __name__=='__main__':
    app.run_server(host='127.0.0.1', port='8050',debug=True)