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
#avg_format = Format()
#avg_format = avg_format.scheme(Scheme.fixed).precision(1).group(Group.yes)
gbp_format = Format()
gbp_format = gbp_format.scheme(Scheme.fixed).precision(2).symbol(Symbol.yes).symbol_prefix('£').group(Group.yes)

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
            data=df.to_dict('records'),
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
            sort_by=[{'column_id': 'rhs_id', 'direction': 'desc'}],), width=12))
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