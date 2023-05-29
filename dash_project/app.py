import os
import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html

app = Dash(__name__, external_stylesheets=['styles.css'])

DATA_PATH = os.path.join('..','datasets','raw','Superstore.csv')
store_df = pd.read_csv(DATA_PATH, parse_dates=['Order Date', 'Ship Date'], encoding='latin-1')
data_by_region = pd.read_csv('../datasets/processed/data_by_region.csv')
data_by_segment = pd.read_csv('../datasets/processed/data_by_segment.csv')



app.layout = html.Div(id='main-div',children=[
    #DIV - HEADER
    html.Div(
        html.H1(id='title',
                children='Super Store Report')
    ),
    
    # DIV - FIRST VIZ
    html.Div(  
        className='principal-graph',
        children=[
            dcc.Graph(id='1st-graph',
                      figure={'data':[go.Line(x=store_df['Order Date'].sort_values(),
                                              y=store_df['Sales'])]
                                
                               }
                      )]
    ),   
     
    # DIV - DUAL VIZ
    html.Div(
        className='div-viz',
        children = [
            html.Div(className='bi-viz',
                     children=[
                         dcc.Graph(id='2nd-graph',
                                   figure={'data':[go.Bar(x=data_by_region.index,
                                                          y=data_by_region['Sales'],
                                                          name='Sales by region')],
                                           'layout':go.Layout(title='Sales by region')}
                         )
                     ]
                    ),
            html.Div(className='bi-viz',
                     children=[
                         dcc.Graph(id='3rd-graph',
                                   figure={'data':[go.Bar(x=data_by_segment.index,
                                                          y=data_by_segment['Sales'],
                                                          name='Sales by segment')]}
                         )
                     ]
                    )
        ]
    )

], style={'overflow-y':'hidden'})

  
if __name__=='__main__':
    app.run_server(host='127.0.0.1', port='8050',debug=True)