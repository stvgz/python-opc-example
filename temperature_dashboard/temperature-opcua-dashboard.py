"""
Dashbaord with dash
"""

from dash import Dash
import dash_core_components as dcc
import dash.dependencies as dd
from dash_core_components.Markdown import Markdown
from dash_table import DataTable
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
import datetime

import pandas as pd
import pymongo

app = Dash(__name__)

app.layout= html.Div(
    [
        dcc.Markdown('# OPC UA Temperature'),
        dcc.Graph(
            id = 'chart_temp'
        ),
        dcc.Graph(
            id = 'chart_pressure'
        ),
        dcc.Graph(
            id = 'chart_hist'
        ),

        dcc.Interval(id='interval',interval = 1*1000, n_intervals=0), # as mili seconds
        dcc.Interval(id='interval_x',interval = 1000*1000, n_intervals=0), # as mili seconds

        dcc.Markdown('Table'),
        DataTable(id = 'table_oos',
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
    # [
    #     dd.Output('annotation','relayoutData'),
    #     # dd.Output('annotation','figure')
    # ],
    [
        dd.Output('chart_pressure','figure'),
        dd.Output('chart_temp','figure'),
        dd.Output('chart_hist','figure'),
        # dd.Output('table_oos','columns'),
        # dd.Output('table','data')
    ],
    [

        dd.Input('interval','n_intervals')

    ],

    prevent_initial_call=True
    )
def update_fig(n):

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

    fig = go.Figure()
    fig.add_trace(go.Scatter(
                        x=df['timestamp'],
                        y=df['temperature'],
                        mode = 'lines+markers',
                        marker=dict(color='blue'),
                        name = 'temperature'

                        ))
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
                        x=df['timestamp'],
                        y=df['pressure'],
                        mode = 'lines+markers',
                        marker=dict(color='red'),
                        name = 'pressure'

                        ))

    spec = 1088

    # add spec on chart
    fig2.add_hline(y=spec,name='Spec',line = dict(color='red',dash='longdash'))


    # hist
    fig_hist = px.histogram(df,x='pressure')
    fig_hist.update_layout(title='histogram')

    df_oos = df[df.pressure>=spec]

    # add oos points on chart
    if not df_oos.empty:
        for idx, row in df_oos.iterrows():
            t = row['timestamp']
            y = row['pressure']
            fig2.add_trace(go.Scatter(x=[t], 
                                    y=[y], 
                                    text= [y],
                                    name = 'out_of_spec',
                                    textposition='top center'))



    columns = [ {"name":i,"id":i } for i in df_oos.columns]
    data = df_oos.to_dict('records')

    return fig,fig2,fig_hist



@app.callback(
    # [
    #     dd.Output('annotation','relayoutData'),
    #     # dd.Output('annotation','figure')
    # ],
    [
        # dd.Output('chart_pressure','figure'),
        # dd.Output('chart_temp','figure'),
        dd.Output('table_oos','columns'),
        dd.Output('table_oos','data')
    ],
    [

        dd.Input('interval','n_intervals')

    ],

    # prevent_initial_call=True
    )
def update_fig(n):
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

    
    spec = 1088

    df_oos = df[df.pressure>=spec]

    if not df_oos.empty:
        df_oos =df_oos.drop('_id',axis=1)

        # df = pd.DataFrame(['x'],columns = ['x'])
        columns = [ {"name":i,"id":i } for i in df_oos.columns]
        data = df_oos.to_dict('records')
    else:
        df = pd.DataFrame(['no oos'],columns='x')
        columns = [ {"name":i,"id":i } for i in df.columns]
        data = df.to_dict('records')

    return [columns,data]



if __name__ == '__main__':

    # app.run_server(port = 8003,debug=True)
    # app.run_server(debug=True)
    app.run_server()