
import dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.FLATLY] #['https://codepen.io/chriddyp/pen/bWLwgP.css']
meta_tags_list = [
    {'name': 'og:title', 'content': 'Hortiq: Horticultural intelligence.'},
    {'name': 'og:image', 'content': '/assets/hortiq-logo-black.png'},
    {'name': 'og:url', 'content': 'http://www.hortiq.co.uk/'}
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, title='Hortiq - Horticultural intelligence',
                suppress_callback_exceptions=True, meta_tags=meta_tags_list)
server = app.server