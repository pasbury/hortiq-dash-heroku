
import dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.FLATLY] #['https://codepen.io/chriddyp/pen/bWLwgP.css']
meta_tags_list = [
    {'property': 'og:title', 'content': 'Hortiq: Horticultural intelligence.'},
    {'property': 'og:image', 'content': 'http://www.hortiq.co.uk/assets/hortiq-screenshot_1.9_1.png'},
    {'property': 'og:url', 'content': 'http://www.hortiq.co.uk/'},
    {'property': 'og:description', 'content': 'Market intelligence for growers and online retailers in the horticulture industry.'}
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, title='Hortiq - Horticultural intelligence',
                suppress_callback_exceptions=True, meta_tags=meta_tags_list)
server = app.server