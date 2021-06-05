import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app, server
from apps import home_app, genera_interest_app, genera_gs_app, genera_opp_comp_app, comp_app, supplier_app
import navbar


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home_app.layout
    if pathname == '/apps/genera_interest_app':
        return genera_interest_app.layout
    elif pathname == '/apps/genera_gs_app':
        return genera_gs_app.layout
    elif pathname == '/apps/genera_opp_comp_app':
        return genera_opp_comp_app.layout
    elif pathname == '/apps/comp_app':
        return comp_app.layout
    elif pathname == '/apps/supplier_app':
        return supplier_app.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)