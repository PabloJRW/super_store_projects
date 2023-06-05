import os
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


app = Dash(__name__, external_stylesheets=['styles.css',dbc.themes.BOOTSTRAP])

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
                         dbc.ButtonGroup(
                             id='unidades',
                             children=[dbc.Button("Sales", n_clicks=0), 
                                       dbc.Button("Profit", n_clicks=0), 
                                       dbc.Button("Discount", n_clicks=0),
                                       dbc.Button("Quantity", n_clicks=0)],
                             loading_state='Sales',
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
                                  id='etiquetas',
                                  options=['Region', 'Segment', 'Category', 'Sub-Category'],
                                  value='Region',
                                  style={'display':'flex',
                                         'justifyContent':'space-evenly'}
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
                                                             y=store_df['Sales'])]},                                    
                            )
                        ]
                    ),
             ])

], style={'overflow-y':'hidden'})


@app.callback(Output('1st-graph', 'figure'),
              [Input('unidades', 'value'),
               Input('etiquetas', 'value'),
               Input('date-range-picker', 'start_date'),
               Input('date-range-picker', 'end_date')])
def groupingData(unidad, etiqueta, start_date, end_date):
    """Function that group data by 'group_by' and return percentage variables"""
    
    store_df.sort_values(by='Order Date', inplace=True)
    #Select date range
    date_range_df = store_df[(store_df['Order Date']>=start_date)&(store_df['Order Date']<=end_date)]
    # Grouping data by feat
    grouping = date_range_df.groupby(by=etiqueta).sum().drop('Postal Code', axis=1)
    
    fig = px.bar(x=grouping.index, 
                 y=grouping[unidad])
    
    fig.update_layout(
        title={'text':"{} BY {}".format(unidad.upper(), etiqueta.upper()),
               'x':0.5},
        xaxis_title="{}".format(etiqueta),
        yaxis_title="{}".format(unidad),
    )

    fig.update_traces()

    return fig

  
if __name__=='__main__':
    app.run_server(host='127.0.0.1', port='8050',debug=True)