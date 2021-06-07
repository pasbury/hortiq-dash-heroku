import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_table
from dash_table.Format import Format, Scheme, Symbol, Group

from app import app
import data_helpers as dh
import pandas as pd

# prepare data for data table (will filter in callback later)
# Datatable fomatting
#avg_format = Format()
#avg_format = avg_format.scheme(Scheme.fixed).precision(1).group(Group.yes)
gbp_format = Format()
gbp_format = gbp_format.scheme(Scheme.fixed).precision(2).symbol(Symbol.yes).symbol_prefix('£').group(Group.yes)

# columns for merchant-level table
cols = [
    { 'id':'merchant_name', 'name':['','Supplier'] },
    { 'id':'rhs_id', 'name':['Number of', 'plants'] },
    { 'id':'google_product_title', 'name':['Number of', 'products'] },
    { 'id': 'price na', 'name': ['Average price by product type/size (if known)', 'Not known'], 'type':'numeric', 'format':gbp_format },
    { 'id': 'price plugs', 'name': ['Average price by product type/size (if known)', 'Plugs'], 'type':'numeric', 'format':gbp_format },
    { 'id': 'price 9cm pot', 'name': ['Average price by product type/size (if known)', '9cm pot'], 'type':'numeric', 'format':gbp_format },
    { 'id': 'price 0.5L pot', 'name': ['Average price by product type/size (if known)', '0.5l pt'], 'type':'numeric', 'format':gbp_format },
    { 'id': 'price 1L pot', 'name': ['Average price by product type/size (if known)', '1l pot'], 'type':'numeric', 'format':gbp_format },
    { 'id': 'price 2L pot', 'name': ['Average price by product type/size (if known)', '2l pot'], 'type':'numeric', 'format':gbp_format },
    { 'id': 'price bulb', 'name': ['Average price by product type/size (if known)', 'Bulbs'], 'type':'numeric', 'format':gbp_format },
    { 'id': 'price seeds', 'name': ['Average price by product type/size (if known)', 'Seeds'], 'type':'numeric', 'format':gbp_format },
    { 'id':'price other', 'name': ['Average price by product type/size (if known)', 'Other'], 'type':'numeric', 'format':gbp_format },]

df = dh.gs_genus_comp.reset_index()
genus_options = [ {'label':e, 'value':e} for e in list(df['genus'].unique()) ]
df['id'] = df['merchant_name'] # use in callback to filter table based on selected supplier

# columns for plant-level table
plant_cols = [
#    { 'id':'botanical_name', 'name':'Plant name'},
    {'id': 'google_product_title', 'name': 'Online product title'},
    {'id': 'item_price', 'name': 'Item price'},
    {'id': 'details_and_offers', 'name': 'Details and offers'},
    {'id': 'total_price', 'name': 'Total price'},
    {'id': 'num_suppliers', 'name': 'Num online suppliers'},
    {'id': 'merchant_url_md', 'name': "Supplier's page", 'type': 'text', 'presentation': 'markdown'},
#    {'id': 'detail_page', 'name': 'Link to RHS plant page'},
]

plant_df = dh.gs_plant_comp

layout = dbc.Container([

    dbc.Row(dbc.Col(html.H2('Find Online Suppliers for a Genus'))),
    dbc.Row(dbc.Col(dbc.Form(dbc.FormGroup([dbc.Label("Please select genus:", className="mr-2"),
                                            dbc.Select(id='genus_dropdown', options=genus_options, value='Rosa')], className="mr-3"), inline=True))),
    html.Br(),
    dbc.Row([dbc.Col(dbc.Card(dbc.CardBody([html.H6("Number of suppliers", className="card-title"),html.H4(id="suppliers_p", className="card-text")])), width=3),
             dbc.Col(dbc.Card(dbc.CardBody([html.H6("Number of products", className="card-title"),html.H4(id="products_p", className="card-text")])), width=3),
             dbc.Col(dbc.Card(dbc.CardBody([html.H6("Average price", className="card-title"),html.H4(id="average_price_p", className="card-text")])), width=3)]),
    html.Br(),
    dbc.Row(dbc.Col(dash_table.DataTable(
            id='gs-genus-comp-table',
            #data=df.to_dict('records'),
            columns=cols,
            sort_action="native",
            page_size=15,
            merge_duplicate_headers=True,
            style_cell={'textAlign': 'right', 'font_family': 'lato',},
            style_cell_conditional=[{
                    'if': {'column_id': 'merchant_name'},
                    'textAlign': 'left'
                }],
            style_header={
                'backgroundColor': '#7b8a8b',
                'fontWeight': 'bold',
                'color':'white'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#ecf0f1'
                }
            ],
            sort_by=[{'column_id': 'rhs_id', 'direction': 'desc'}],), width=12)),
    html.Br(),
    dbc.Row(dbc.Col(html.H4('Plants matching selected genus and supplier'))),
    dbc.Row(dbc.Col(html.H6('Please click on a row in the table above in order to select a supplier.'))),
    html.Br(),
    dbc.Row(dbc.Col(dash_table.DataTable(
        id='gs-plant-comp-table',
        data=plant_df.to_dict('records'),
        columns=plant_cols,
        sort_action="native",
        page_size=15,
        style_cell={'textAlign': 'right', 'font_family': 'lato', 'overflow': 'hidden', 'textOverflow': 'ellipsis', 'maxWidth': 12,},
        style_cell_conditional=[{
            'if': {'column_id': 'google_product_title'},
            'textAlign': 'left',
            'width': '40%',
        },
        {
            'if': {'column_id': 'details_and_offers'},
            'width': '25',
        }
        ],
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
        ), width=12)),
    ])


@app.callback(Output('suppliers_p', 'children'),
              Output('products_p', 'children'),
              Output('average_price_p', 'children'),
              Output('gs-genus-comp-table', 'data'),
              Input('genus_dropdown', 'value'))
def filter_table(value):
    if value:
        # filter dataframe based on selection
        fdf = df[df.genus.isin(([value])) & (df.rhs_id > 1)]
        num_suppliers_str = '{:,}'.format(len(fdf))
        num_products_str = '{:,}'.format(int(sum(fdf['google_product_title'])))
        average_price = sum(fdf['item_price_num'])/sum(fdf['google_product_title']) if sum(fdf['google_product_title']) > 0 else 0
        average_price_str = '£{:,.2f}'.format(average_price)
    else:
        fdf = df
        num_suppliers_str = ""
        num_products_str = ""
        average_price_str = ""
    return num_suppliers_str, num_products_str, average_price_str, fdf.to_dict('records')

@app.callback(
              Output('gs-plant-comp-table', 'data'),
              Output('gs-plant-comp-table', 'tooltip_data'),
              Input('gs-genus-comp-table', 'active_cell'),
              State('genus_dropdown', 'value'),
              State('gs-genus-comp-table', 'data'),
              State('gs-plant-comp-table', 'columns'),
)
def filter_plant_table(active_cell, value, data, table_columns):
    if value and active_cell:
        # filter dataframe based on selection
        selected_supplier = active_cell['row_id']
        fdf = plant_df[plant_df.genus.isin(([value])) & (plant_df['merchant_name'] == selected_supplier)]
        fdf['merchant_url_md'] = '[Link]' + '(' + fdf['merchant_url'] + ')'

        # tooltips
        col_list = [column['id'] for column in table_columns]
        tooltip_data = [{c: {'type': 'text', 'value': f'{r[c]}'} for c in col_list} for r in fdf[col_list].to_dict(orient='records')]

    else:
        fdf = pd.DataFrame()
        tooltip_data = []

    return fdf.to_dict('records'), tooltip_data