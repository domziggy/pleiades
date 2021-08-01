# File that pulls the directory together to run the entire application
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash

from frontEnd.homepage import *
from frontEnd.eda_page import *

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.config.suppress_callback_exceptions = True
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Store(id='index_input', storage_type='session')
])

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/eda_page':
        return eda_layout()
    else:
        return home_layout()
    
if __name__ == '__main__':
    app.run_server(debug=True)