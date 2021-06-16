"""
Dashbaord with dash
"""

from dash import Dash
import dash_core_components as dcc
from dash.dependencies import Input,Output
import dash_html_components as html
import plotly.graph_objs as go
import datetime

import pandas as pd
import pymongo

app = Dash()

app.layout= html.Div(
    [
        dcc.Markdown('# OPC UA Temperature'),
        dcc.Graph(
            id = 'temperature'
        ),

        dcc.Interval(id='interval',interval = 1000) # as mili seconds
    ] 
)


## mongo db 
# mongodb connection

mongo_client = pymongo.MongoClient("mongodb://admin:IoTadmin!@101.200.42.133:27017/")

# db
db = mongo_client["opc"]

# collection
col_temperature = db['temperature']


@app.callback(
    Output('temperature','figure'),
    Input('interval','n_intervals')
)
def update(n):

    fig = go.Figure()
    
    # get information from opc directly or db, most recent value
    time_start  = datetime.datetime.now() - datetime.timedelta(hours=1)

    query  = {
        "timestamp":{
            "$gte": time_start
        }
    }

    r = col_temperature.find(query)
    df = pd.DataFrame([v for v in r])

    fig.add_trace(go.Scatter(
                        x=df['timestamp'],
                        y=df['temperature'],
                        mode = 'lines+markers',
                        marker=dict(color='blue'),
                        name = 'temperature'

                        ))
    
    fig.add_trace(go.Scatter(
                        x=df['timestamp'],
                        y=df['pressure'],
                        mode = 'lines+markers',
                        marker=dict(color='red'),
                        name = 'pressure'

                        ))

    return fig

if __name__ == '__main__':

    app.run_server(port = 8003)