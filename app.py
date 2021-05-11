
import dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.FLATLY] #['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, title='Hortiq - Horticultural intelligence', suppress_callback_exceptions=True)
server = app.server