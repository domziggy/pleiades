import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from . import page_components

nbar = page_components.navigationBar()

body = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2('Heading'), 
            html.P('The kittens feast during the fall time.'),
            dbc.Button('View details', color='secondary')
        ], md=4),
        dbc.Col([
            html.H2('Graph'),
            dcc.Graph(figure={
                'data': [{'x': [1,5,3], 'y':[2,2,5]}]
            })
        ])
    ])
], className='mt-4')

def eda_layout():
    layout = html.Div([
        nbar, 
        body
    ])

    return layout