import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from . import utils

nbar = utils.navigationBar()

body = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2('Heading'), 
            html.P('The moose run wild during the winter time.'),
            dbc.Button('View details', color='secondary')
        ], md=4),
        dbc.Col([
            html.H2('Graph'),
            dcc.Graph(figure={
                'data': [{'x': [1,2,3], 'y':[3,2,1]}]
            })
        ])
    ])
], className='mt-4')

def home_layout():
    layout = html.Div([
        nbar, 
        body
    ])

    return layout
