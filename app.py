import os
import json

import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import plotly.express as px

# Load data

# read relative interest file
try:
    infile='data/genera_relative_interest.txt'
    with open(infile, 'r') as infile:
        indata = infile.read()
    interest = json.loads(indata)
except FileNotFoundError as fnf_error:
    print(fnf_error)
# prepare dataframe to plot
d = {k: {'relative_interest': v['relative_interest'], 'yoy_1Y_pct': v['yoy_1Y_pct']} for k, v in interest.items()}
df = pd.DataFrame(d).transpose()
df['label'] = df.index
df = df.query('-0.2 <= yoy_1Y_pct <= 1')

fig = px.scatter(df,x='relative_interest',y='yoy_1Y_pct', text='label', log_x=True, height=800, width = 800)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H2('Hortiq'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value'),
    dcc.Graph(id='scatter-plot', figure=fig)
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)