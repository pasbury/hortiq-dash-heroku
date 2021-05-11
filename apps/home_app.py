import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

layout = html.Div([
    html.H3('Hortiq Home Page'),
    dcc.Link('Go to Genus-Level Search Interest Dashboard', href='/apps/genera_interest_app'),
    html.Br(),
    dcc.Link('Go to Genus-Level Online Buying Options Dashboard', href='/apps/genera_gs_app'),
    html.Br(),
    dcc.Link('Go to Genus-Level opportunity vs Competitiveness', href='/apps/genera_opp_comp_app')
    ])