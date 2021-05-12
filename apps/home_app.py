import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app

layout = dbc.Container([
    dbc.Row([dbc.Col(html.H3('Welcome to Hortiq: Horticultural intelligence'))]),
    dbc.Row([dbc.Col(html.P('Hortiq is a new service for growers and retailers in horticultural industry.  We aim to provide provide information to help with decisions about assortment, pricing and online marketing.'))]),
    html.Br(),
    dbc.Row([dbc.Col(html.P("This site is a 'proof of concept'.  We would really appreciate feedback and suggestions.  So please take a look and share your thoughts via contact.us@hortiq.co.uk"))]),
    html.Br(),
    dcc.Link('Go to Genus-Level Search Interest Dashboard', href='/apps/genera_interest_app'),
    html.Br(),
    dcc.Link('Go to Genus-Level Online Buying Options Dashboard', href='/apps/genera_gs_app'),
    html.Br(),
    dcc.Link('Go to Genus-Level opportunity vs Competitiveness', href='/apps/genera_opp_comp_app')
    ])