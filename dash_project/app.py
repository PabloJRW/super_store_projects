import os
import pandas as pd
import plotly.graph_objs as go
from dash import Dash, dcc, html

app = Dash(__name__, external_stylesheets=['styles.css'])

DATA_PATH = os.path.join('..','datasets','raw','Superstore.csv')
store_df = pd.read_csv(DATA_PATH, parse_dates=['Order Date', 'Ship Date'])
store_df.set_index('Date Order', inplace=True)


app.layout = html.Div([
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
                      figure={'data':[go.Box(
                                              y=store_df['Sales'])]}
                      )]
    ),   
     
    # DIV - DUAL VIZ
    html.Div(
        className='div-viz',
        children = [
            html.Div(className='bi-viz',
                     children=[
                         dcc.Graph(id='2nd-graph')]
                    ),
            html.Div(className='bi-viz',
                     children=[
                         dcc.Graph(id='3rd-graph')]
                    )
        ]
    )

])


if __name__=='__main__':
    app.run_server(host='127.0.0.1', port='8050',debug=True)