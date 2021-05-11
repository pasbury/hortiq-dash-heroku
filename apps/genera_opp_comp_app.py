import dash_core_components as dcc
import dash_html_components as html
import dash
#from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_table
from dash_table.Format import Format, Scheme, Symbol, Group

import pandas as pd
import numpy as np
import plotly.express as px

from app import app
import data_helpers as dh


# Get genus-level Google Shopping data, and genus-level search interest data
# Interest...
d = {k: {'relative_interest': v['relative_interest'], 'yoy_1Y_pct': v['yoy_1Y_pct']} for k, v in dh.interest.items()}
df = pd.DataFrame(d).transpose()
df['genus'] = df.index
with np.errstate(divide='ignore'):
    df['log_relative_interest'] = np.where(df['relative_interest'] > 0, np.log10(df['relative_interest']), np.nan )
lri_min = df['log_relative_interest'].min()
lri_max = df['log_relative_interest'].max()
scale_max = 100
df['scaled_relative_interest'] = ( df['log_relative_interest'] - lri_min ) * scale_max / ( lri_max - lri_min )
# Join to genus-level google shopping data
df = pd.merge(left=dh.gs_genus, right=df, how='inner', on='genus')

opp_options = [
    { 'label':'Average price', 'value':'avg_gs_price' },
    { 'label':'Num plants with AGM', 'value':'num_agm_plants'},
    { 'label':'Change in search volume, last 12 months vs prior 12 months', 'value': 'yoy_1Y_pct'},
    { 'label':'Search volume in last 12 months', 'value': 'scaled_relative_interest'},
]

comp_options = [
    { 'label':'Avg RHS-listed suppliers', 'value':'avg_rhs_suppliers' },
    { 'label':'Avg Google Shopping suppliers', 'value':'avg_gs_suppliers'},
]

layout = dbc.Container([

    dbc.Row(dbc.Col(html.H2('Explore Growth Opportunities in Popular Plant Genera'))),
    dbc.Row(dbc.Col(html.H6('Filter genera by plant type in this dropdown:'))),
    dbc.Row(dbc.Col(dcc.Dropdown(
        id='type_dropdown',
        options=dh.plant_type_options,
        value=['All Types'],
        multi=True
    ), width=6)),
    html.Br(),
    dbc.Row(dbc.Col(html.H6("Please select metrics for 'opportunity' and 'competitive intensity'"))),
    dbc.Row([dbc.Col([html.H6("Opportunity metric:"),dcc.Dropdown(id='opp-dropdown', options=opp_options, value='avg_gs_price')]),
            dbc.Col([html.H6("Competitive intensity metric:"),dcc.Dropdown(id='comp-dropdown', options=comp_options, value='avg_gs_suppliers')])]),
    dbc.Row(dbc.Col(dcc.Graph(id='bubble-plot')))
    ])


@app.callback(dash.dependencies.Output('bubble-plot', 'figure'),
              [dash.dependencies.Input('type_dropdown', 'value'),dash.dependencies.Input('opp-dropdown', 'value'),dash.dependencies.Input('comp-dropdown', 'value')])
def update_bubble(types, opp_metric, comp_metric):
    # filter dataframe based on selection
    filter_list = dh.genera_to_show(dh.genera_dict, types)
    fdf = df[df.genus.isin(filter_list)]

    # axis labels, depending on chosen metrics
    labels = {
        'avg_gs_price': 'Average item price (£)',
        'avg_gs_suppliers': 'Average number of suppliers per plant',
        'avg_rhs_suppliers': 'Average number of RHS-listed suppliers per plant',
        'num_agm_plants': 'Num plants with AGM',
        'yoy_1Y_pct': 'Change in search volume, last 12 months vs prior 12 months',
        'scaled_relative_interest': 'Search volume in last 12 months'
    }
    # create the plot
    fig = px.scatter(fdf, x=comp_metric, y=opp_metric,
                     size="num_agm_plants", hover_name="genus", size_max=60,
                     labels={
                         comp_metric: labels[comp_metric],
                         opp_metric: labels[opp_metric]
                     },
                     title="Google Shopping: Opportunity vs Competitive Intensity")

    return fig