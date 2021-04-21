import os
import json

import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd
import plotly.express as px

# Load data
# read the master genera data file
try:
    infile='data/genera_master.txt'
    with open(infile, 'r') as infile:
        indata = infile.read()
    genera_dict = json.loads(indata)
except FileNotFoundError as fnf_error:
    print(fnf_error)
# read relative interest file
try:
    infile='data/genera_relative_interest.txt'
    with open(infile, 'r') as infile:
        indata = infile.read()
    interest = json.loads(indata)
except FileNotFoundError as fnf_error:
    print(fnf_error)

# get the options for plant types
plant_types = set()
[plant_types.update(v['plant_types']) for k,v in genera_dict.items()]
plant_type_options = [ {'label':e, 'value':e} for e in plant_types ]

# get lookup of genera for each plant type
type_to_genera = {}
for g,v in genera_dict.items():
    for t in v['plant_types']:
        if t not in type_to_genera:
            type_to_genera[t] = []
        type_to_genera[t].append(g)

# prepare dataframe to plot
d = {k: {'relative_interest': v['relative_interest'], 'yoy_1Y_pct': v['yoy_1Y_pct']} for k, v in interest.items()}
df = pd.DataFrame(d).transpose()
df['label'] = df.index
df = df.query('-0.2 <= yoy_1Y_pct <= 1')
# create the plot
fig = px.scatter(df,x='relative_interest',y='yoy_1Y_pct', text='label', log_x=True, height=800, width = 800)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H2('Hortiq'),
    dcc.Dropdown(
        id='dropdown',
        options=plant_type_options,
        value=['All Types'],
        multi=True
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