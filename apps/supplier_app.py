import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_table
from dash_table.Format import Format, Scheme, Symbol, Group

from app import app
import data_helpers as dh

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

layout = dbc.Container([

    dbc.Row(dbc.Col(html.H2('Find Genera Offered Online by a Supplier'))),
    dbc.Row(dbc.Col(dbc.Form(dbc.FormGroup([dbc.Label("Please select supplier:", className="mr-2"),
                                            dbc.Select(id='supplier_dropdown', options=supplier_options, value=['Crocus.co.uk'])], className="mr-3"), inline=True))),
    html.Br(),
    dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Number of genera", className="card-title"),html.H4(id="genera_p", className="card-text")])), width=3),
        dbc.Col(dbc.Card(dbc.CardBody([html.H6("Number of products", className="card-title"),html.H4(id="supplier_products_p", className="card-text")])), width=3),
    #    dbc.Col(dbc.Card(dbc.CardBody([html.H6("Average price", className="card-title"),html.H4(id="average_price_p", className="card-text")])), width=3)
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
            sort_by=[{'column_id': 'rhs_id', 'direction': 'desc'}],), width=12))
    ])

@app.callback(
    Output('genera_p', 'children'),
              Output('supplier_products_p', 'children'),
    #           Output('average_price_p', 'children'),
              Output('supplier-lookup-table', 'data'),
              Input('supplier_dropdown', 'value'))
def filter_table(value):
    if value:
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
    return num_genera_str, num_products_str, fdf.to_dict('records')

#, average_price_str,