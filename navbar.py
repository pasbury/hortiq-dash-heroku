import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app

# building the navigation bar
# https://github.com/facultyai/dash-bootstrap-components/blob/master/examples/advanced-component-usage/Navbars.py
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Search Interest", href='/apps/genera_interest_app'),
        dbc.DropdownMenuItem("Online Buying - Summary Level", href='/apps/genera_gs_app'),
        dbc.DropdownMenuItem("Online Buying - Opportunity", href='/apps/genera_opp_comp_app'),
        dbc.DropdownMenuItem("Compare Suppliers", href='/apps/comp_app'),
    ],
    nav = True,
    in_navbar = True,
    label = "Dashboards",
)


navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/hortiq-logo-white.png", height="60px")),
                        #dbc.Col(dbc.NavbarBrand("Hortiq", className="ml-2")),
                    ],
                    align="centre",
                    justify="start",
                    no_gutters=True,
                ),
                href="/",
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dbc.NavItem(dbc.NavLink("Home", href="/")),dbc.NavItem(dbc.NavLink("About", href="/about")),dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ]),
    color="dark",
    dark=True,
    className="mb-4",
    #className="ml-0",
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)(toggle_navbar_collapse)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])