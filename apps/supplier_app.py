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
gbp_format = Format()
gbp_format = gbp_format.scheme(Scheme.fixed).precision(2).symbol(Symbol.yes).symbol_prefix('£').group(Group.yes)

cols = [
    { 'id':'genus', 'name':['','Genus'] },
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
supplier_options = [ {'label':e, 'value':e} for e in list(df['merchant_name'].unique()) ]
df['id'] = df['genus'] # use in callback to filter table based on selected genus

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

    dbc.Row(dbc.Col(html.H2('Find Genera Offered Online by a Supplier'))),
    dbc.Row(dbc.Col(dbc.Form(dbc.FormGroup([dbc.Label("Please select supplier:", className="mr-2"),
                                            dbc.Select(id='supplier_dropdown', options=supplier_options, value="Crocus.co.uk")], className="mr-3"), inline=True))),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Number of genera", className="card-title"),html.H4(id="genera_p", className="card-text")])), width=3),
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Number of products", className="card-title"),html.H4(id="supplier_products_p", className="card-text")])), width=3),
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Average price", className="card-title"),html.H4(id="supplier_average_price_p", className="card-text")])), width=3)
    ]),
    html.Br(),
    dbc.Row(dbc.Col(dash_table.DataTable(
            id='supplier-lookup-table',
            data=df.to_dict('records'),
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
    dbc.Row(dbc.Col(html.H6('Please click on a row in the table above in order to select a genus.'))),
    html.Br(),
    dbc.Row(dbc.Col(dash_table.DataTable(
        id='gs-plant-supplier-table',
        data=[],
        columns=plant_cols,
        # css=[dict(selector='td[data-dash-column="merchant_url_md"] table', rule='text-align: centre;')],
        sort_action="native",
        page_size=15,
        style_cell={'textAlign': 'right', 'font_family': 'lato', 'overflow': 'hidden', 'textOverflow': 'ellipsis',
                    'maxWidth': 12, },
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

@app.callback(
    Output('genera_p', 'children'),
              Output('supplier_products_p', 'children'),
              Output('supplier_average_price_p', 'children'),
              Output('supplier-lookup-table', 'data'),
              Input('supplier_dropdown', 'value'))
def filter_table(value):
    if not (value is None):
        # filter dataframe based on selection
        fdf = df[df['merchant_name'].isin(([value])) & (df.rhs_id > 1)]
        num_genera_str = '{:,}'.format(len(fdf))
        num_products_str = '{:,}'.format(int(sum(fdf['google_product_title'])))
        average_price = sum(fdf['item_price_num'])/sum(fdf['google_product_title']) if sum(fdf['google_product_title']) > 0 else 0
        average_price_str = '£{:,.2f}'.format(average_price)
    else:
        fdf = df
        num_genera_str = ""
        num_products_str = ""
        average_price_str = ""
    return num_genera_str, num_products_str, average_price_str, fdf.to_dict('records')


@app.callback(
              Output('gs-plant-supplier-table', 'data'),
              Output('gs-plant-supplier-table', 'tooltip_data'),
              Input('supplier-lookup-table', 'active_cell'),
              State('supplier_dropdown', 'value'),
              State('gs-plant-supplier-table', 'columns'),
)
def filter_plant_table(active_cell, value, table_columns):
    if value and active_cell:
        # filter dataframe based on selection
        selected_genus = active_cell['row_id']
        fdf = plant_df[plant_df['merchant_name'].isin(([value])) & (plant_df['genus'] == selected_genus)]
        fdf['merchant_url_md'] = '[Link]' + '(' + fdf['merchant_url'] + ')'

        # tooltips
        col_list = [column['id'] for column in table_columns]
        tooltip_data = [{c: {'type': 'text', 'value': f'{r[c]}'} for c in col_list} for r in fdf[col_list].to_dict(orient='records')]

    else:
        fdf = pd.DataFrame()
        tooltip_data = []

    return fdf.to_dict('records'), tooltip_data