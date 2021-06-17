"""
Dashbaord with dash
"""

from dash import Dash
import dash_core_components as dcc
from dash.dependencies import Input,Output
from dash_core_components.Markdown import Markdown
from dash_table import DataTable
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

        dcc.Interval(id='interval',interval = 50*1000, n_intervals=0), # as mili seconds

        dcc.Markdown('Table'),
        DataTable(id = 'table',
                    columns=[])


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
    [
        Output('temperature','figure'),
        # Output('table','columns'),
        # Output('table','data')
    ],   
    [Input('interval','n_intervals')]
)
def update(n):

    fig = go.Figure()
    
    # get information from opc directly or db, most recent value
    time_start  = datetime.datetime.now() - datetime.timedelta(hours=24)
    
    query  = {
        "timestamp":{
            "$gte": time_start
            }
        }

    # r = col_temperature.find(query)

    # client = MongoClient('mongodb://admin:IoTadmin%21@101.200.42.133:27017/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&ssl=false')
    filter={}
    sort=list({
        'timestamp': -1
    }.items())
    limit=100

    result = mongo_client['opc']['temperature'].find(
        filter=filter,
        sort=sort,
        limit=limit
        )


    df = pd.DataFrame([v for v in result])

    print(df.shape)
    # limit to last 200 points
    df=df.tail(100)


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

    spec = 1088

    df_oos = df[df.pressure>=spec]

    columns = [ {"name":i,"id":i } for i in df_oos.columns]
    data = df_oos.to_dict('records')

    # return [fig, columns, data]
    return [fig]

if __name__ == '__main__':

    # app.run_server(port = 8003,debug=True)
    # app.run_server(debug=True)
    app.run_server()