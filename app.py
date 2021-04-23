import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

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

# get lookup of genera to display, given selected plant types
def genera_to_show(genera_dict, types):
    type_to_genera = {}
    for g, v in genera_dict.items():
        for t in v['plant_types']:
            if t not in type_to_genera:
                type_to_genera[t] = []
            type_to_genera[t].append(g)

    distinct_genera = set()
    [distinct_genera.update(type_to_genera[t]) for t in types]
    return sorted(distinct_genera)

# prepare dataframe to plot
d = {k: {'relative_interest': v['relative_interest'], 'yoy_1Y_pct': v['yoy_1Y_pct']} for k, v in interest.items()}
df = pd.DataFrame(d).transpose()
df['label'] = df.index
df = df.query('-0.2 <= yoy_1Y_pct <= 1')

external_stylesheets = external_stylesheets=[dbc.themes.BOOTSTRAP] #['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,title='Hortiq - Horticultural intelligence')
server = app.server

card_with_tabs = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Top", tab_id="tab-top"),
                    dbc.Tab(label="Rising", tab_id="tab-rising"),
                    dbc.Tab(label="Suggestions", tab_id="tab-suggestions")
                ],
                id="card-tabs",
                card=True,
                active_tab="tab-top",
            )
        ),
        dbc.CardBody(html.P(id="card-content", className="card-text")),
    ]
)

div_with_tabs = html.Div([
    html.P('Related search queries'),
    dbc.Tabs(
        [
            dbc.Tab(label="Top", tab_id="tab-top"),
            dbc.Tab(label="Rising", tab_id="tab-rising"),
            dbc.Tab(label="Suggestions", tab_id="tab-suggestions")
        ],
        id="card-tabs",
        card=True,
        active_tab="tab-top"
    ),
    html.Div(id='card-content')]
)

app.layout = html.Div([

    dbc.Row(dbc.Col(html.H2('Hortiq'))),
    dbc.Row(dbc.Col(html.H6('Horticultural intelligence.'))),
    dbc.Row(dbc.Col(dcc.Dropdown(
        id='dropdown',
        options=plant_type_options,
        value=['All Types'],
        multi=True
    ), width=6)),
    dbc.Row([
        dbc.Col(dcc.Graph(id='scatter-plot', clickData={'points': [{'text': 'Roses'}]}), width=5),
        dbc.Col([
            dbc.Row(dbc.Col(dcc.Graph(id='line-plot'))),
            dbc.Row(dbc.Col(html.Div([html.P('Related search queries'),card_with_tabs])))
        ], width=5)
    ])
])

@app.callback(dash.dependencies.Output('scatter-plot', 'figure'),
              dash.dependencies.Input('dropdown', 'value'))
def update_scatter(value):
    # filter dataframe based on selection
    filter_list = genera_to_show(genera_dict, value)
    fdf = df[df.index.isin(filter_list)]
    # create the plot
    fig = px.scatter(fdf, x='relative_interest', y='yoy_1Y_pct', text='label', log_x=True, height=800, width=800,
                     labels={
                         "relative_interest": "Search volume in last 12 months (log scale)",
                         "yoy_1Y_pct": "Change in search volume, last 12 months vs prior 12 months"
                     },
                     title="Google Search Volume by Genus")
    fig.update_yaxes(tickformat='%')
    fig.update_xaxes(showticklabels=False)

    return fig

@app.callback(dash.dependencies.Output('line-plot', 'figure'),
              dash.dependencies.Input('scatter-plot', 'clickData'))
def update_line(clickData):
    # get genus that has been clicked
    g = clickData['points'][0]['text']
    # get iot data for that genus
    df = pd.DataFrame(interest[g]['iot'])
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    # create the plot
    fig = px.line(df, x=df.index, y=df.columns[0], title=g + ': Search interest over last five years',height=400, width = 850, labels = {'index':'Date', df.columns[0]:'Search volume (maximum = 100)'})

    return fig

@app.callback(dash.dependencies.Output("card-content", "children"), [dash.dependencies.Input("card-tabs", "active_tab"),
                                                                     dash.dependencies.Input('scatter-plot', 'clickData')])
def tab_content(active_tab, clickData):
    # get genus that has been clicked
    g = clickData['points'][0]['text']
    if active_tab == 'tab-suggestions':
        content = [ html.P(i, style={'line-height':0.7}) for i in interest[g]['suggested_queries'] ]
    elif active_tab == 'tab-top':
        df = pd.DataFrame(interest[g]['related_queries_top'])
        content = dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df.columns],
            page_size=6)
    else: # tab-rising
        df = pd.DataFrame(interest[g]['related_queries_rising'])
        content = dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df.columns],
            page_size=6)
    return content


if __name__ == '__main__':
    app.run_server(debug=True)