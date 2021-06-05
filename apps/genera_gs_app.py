import dash_core_components as dcc
import dash_html_components as html
import dash
#from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_table
from dash_table.Format import Format, Scheme, Symbol, Group

import pandas as pd
import plotly.express as px

from app import app
import data_helpers as dh

# prepare data for data table (will filter in callback later)
# Datatable fomatting
avg_format = Format()
avg_format = avg_format.scheme(Scheme.fixed).precision(1).group(Group.yes)
gbp_format = Format()
gbp_format = gbp_format.scheme(Scheme.fixed).precision(2).symbol(Symbol.yes).symbol_prefix('£').group(Group.yes)

cols = [
    { 'id':'genus', 'name':['','Genus'] },
    { 'id':'num_plants', 'name':['Number of plants', 'In scope'] },
    { 'id':'num_agm_plants', 'name':['Number of plants', 'With AGM'] },
    { 'id':'avg_rhs_suppliers', 'name':['','Avg RHS-listed suppliers'], 'type':'numeric', 'format':avg_format },
    { 'id':'num_gs_plants', 'name':['Google Shopping Results','Num plants'] },
    { 'id':'num_gs_suppliers', 'name': ['Google Shopping Results', 'Num suppliers']},
    { 'id':'avg_gs_suppliers', 'name': ['Google Shopping Results', 'Avg num suppliers'], 'type':'numeric', 'format':avg_format },
    {'id':'num_gs_products', 'name': ['Google Shopping Results', 'Num products']},
    {'id':'avg_gs_price', 'name': ['Google Shopping Results', 'Avg price'], 'type':'numeric', 'format':gbp_format } ]
# '0.5L pot',
# '1L pot',
# '2L pot',
# '3L pot',
# '9cm pot',
# 'other',
# 'bulb',
# 'na',
# 'plugs',
# 'seeds',
keep_cols = [ i['id'] for i in cols ]
df = dh.gs_genus.loc[:,keep_cols]

layout = dbc.Container([

    dbc.Row(dbc.Col(html.H2('Compare Online Buying Options for Popular Plant Genera'))),
    dbc.Row(dbc.Col(html.H6('Filter genera by plant type in this dropdown:'))),
    dbc.Row(dbc.Col(dcc.Dropdown(
        id='dropdown',
        options=dh.plant_type_options,
        value=['All Types'],
        multi=True
    ), width=6)),
    html.Br(),
    dbc.Row(dbc.Col(html.H4('Buying options from Google Shopping'))),
    dbc.Row(dbc.Col(dash_table.DataTable(
            id='gs-genus-table',
            data=df.to_dict('records'),
            #columns=[{'id': c, 'name': c} for c in df.columns],
            columns=cols,
            sort_action="native",
            page_size=15,
            merge_duplicate_headers=True,
            style_cell={'textAlign': 'right', 'font_family': 'lato',},
            style_cell_conditional=[{
                    'if': {'column_id': 'genus'},
                    'textAlign': 'left'
                }],
            style_header={
                'backgroundColor': '#7b8a8b',
                'fontWeight': 'bold',
                'color': 'white'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#ecf0f1'
                }
            ],
           ), width=8))
    ])


@app.callback(dash.dependencies.Output('gs-genus-table', 'data'),
              dash.dependencies.Input('dropdown', 'value'))
def filter_table(value):
    # filter dataframe based on selection
    filter_list = dh.genera_to_show(dh.genera_dict, value)
    fdf = df[df.genus.isin(filter_list)]

    return fdf.to_dict('records')

