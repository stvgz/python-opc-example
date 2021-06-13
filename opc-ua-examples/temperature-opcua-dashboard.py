"""
Dashbaord with dash
"""

from dash import Dash
import dash_core_components as dcc
from dash.dependencies import Input,Output
import dash_html_components as html
import plotly.graph_objs as go

app = Dash()

app.layout= html.Div(
    [
        dcc.Markdown('# OPC UA Temperature'),
        dcc.Graph(
            id = 'temperature'
        ),

        dcc.Interval(id='interval',interval = 10) # as mili seconds
    ] 
)

@app.callback(
    Output('temperature','figure'),
    Input('interval','n_interval')
)
def update(n):

    fig = go.figure()

    # get information from opc

    return fig

if __name__ == '__main__':

    app.run_server()