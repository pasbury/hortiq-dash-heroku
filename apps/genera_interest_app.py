import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table

import pandas as pd
import plotly.express as px

from app import app

import data_helpers as dh


# remove irrelevant results from 'buy suggestions'
def process_buy_sugg(in_list, search_prefix):
    out_list = []
    for s in in_list:
        x = s.split(search_prefix + ' ')
        if len(x) > 1:
            out_list.append(search_prefix + ' ' + x[1])
    return out_list

# prepare dataframe to plot
d = {k: {'relative_interest': v['relative_interest'], 'yoy_1Y_pct': v['yoy_1Y_pct']} for k, v in dh.interest.items()}
df = pd.DataFrame(d).transpose()
df['label'] = df.index
df = df.query('-0.2 <= yoy_1Y_pct <= 1')


card_with_tabs = dbc.Card(
    [
        dbc.CardHeader(
            dbc.Tabs(
                [
                    dbc.Tab(label="Top", tab_id="tab-top"),
                    dbc.Tab(label="Rising", tab_id="tab-rising"),
                    dbc.Tab(label="Suggestions", tab_id="tab-suggestions"),
                    dbc.Tab(label="'Buy..' suggestions", tab_id="tab-buy")
                ],
                id="card-tabs",
                card=True,
                active_tab="tab-top",
            )
        ),
        dbc.CardBody(html.P(id="card-content", className="card-text")),
    ]
)
layout = dbc.Container([

    dbc.Row(dbc.Col(html.H2('Online Search Interest for Popular Plant Genera'))),
    html.Br(),
    dbc.Row(dbc.Col(html.H6('Filter genera by plant type in this dropdown:'))),
    dbc.Row(dbc.Col(dcc.Dropdown(
        id='dropdown',
        options=dh.plant_type_options,
        value=['All Types'],
        multi=True
    ), width=6)),
    html.Br(),
    dbc.Row([
        dbc.Col(dcc.Graph(id='scatter-plot', clickData={'points': [{'text': 'Roses'}]}), width=7),
        dbc.Col([
            dbc.Row(dbc.Col(dcc.Graph(id='line-plot'))),
        ], width=5)
    ]),
    html.Br(),
    dbc.Row(dbc.Col(html.Div([html.P('Related search queries'),card_with_tabs])))
])

@app.callback(dash.dependencies.Output('scatter-plot', 'figure'),
              dash.dependencies.Input('dropdown', 'value'))
def update_scatter(value):
    # filter dataframe based on selection
    filter_list = dh.genera_to_show(dh.genera_dict, value)
    fdf = df[df.index.isin(filter_list)]
    # create the plot
    fig = px.scatter(fdf, x='relative_interest', y='yoy_1Y_pct', text='label', log_x=True,
                     labels={
                         "relative_interest": "Search volume in last 12 months (log scale)",
                         "yoy_1Y_pct": "Change in search volume, last 12 months vs prior 12 months"
                     },
                     title="Google Search Volume by Genus")
    fig.update_yaxes(tickformat='%')
    fig.update_xaxes(showticklabels=False)
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10)
    )

    return fig

#height=600, width=600,

@app.callback(dash.dependencies.Output('line-plot', 'figure'),
              dash.dependencies.Input('scatter-plot', 'clickData'))
def update_line(clickData):
    # get genus that has been clicked
    g = clickData['points'][0]['text']
    # get iot data for that genus
    df = pd.DataFrame(dh.interest[g]['iot'])
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    # create the plot
    fig = px.line(df, x=df.index, y=df.columns[0], title=g + ': Search interest over last five years', labels = {'index':'Date', df.columns[0]:'Search volume (maximum = 100)'})
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10)
    )
    return fig
#height=400, width = 600,
@app.callback(dash.dependencies.Output("card-content", "children"), [dash.dependencies.Input("card-tabs", "active_tab"),
                                                                     dash.dependencies.Input('scatter-plot', 'clickData')])
def tab_content(active_tab, clickData):
    # get genus that has been clicked
    g = clickData['points'][0]['text']
    if active_tab == 'tab-suggestions':
        content = html.Ol([ html.Li(i) for i in dh.interest[g]['suggested_queries'] ])
    elif active_tab == 'tab-buy':
        content = html.Ol([html.Li(i) for i in process_buy_sugg(dh.interest[g]['suggested_queries_buy'],
                                                                'buy ' + dh.genera_dict[g]['botanical_name'].lower())])
    elif active_tab == 'tab-top':
        df = pd.DataFrame(dh.interest[g]['related_queries_top'])
        content = dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df.columns],
            page_size=6,
            style_cell_conditional = [{
                'if': {'column_id': 'query'},
                'textAlign': 'left'
            }])
    else: # tab-rising
        df = pd.DataFrame(dh.interest[g]['related_queries_rising'])
        content = dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df.columns],
            page_size=6,
            style_cell_conditional = [{
                'if': {'column_id': 'query'},
                'textAlign': 'left'
            }])
    return content