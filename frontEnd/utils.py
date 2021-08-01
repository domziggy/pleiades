import dash_bootstrap_components as dbc

def navigationBar():
    nbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink('Homepage', href='/homepage')),
            dbc.NavItem(dbc.NavLink('Exploration', href='/eda_page')),
            dbc.NavItem(dbc.NavLink('Regression', href='/homepage')),
            dbc.NavItem(dbc.NavLink('Classification', href='/homepage')),
            dbc.NavItem(dbc.NavLink('Unsupervised', href='/homepage')),
            dbc.NavItem(dbc.NavLink('Model Selection', href='/homepage'))
        ],
        brand='Home',
        brand_href='/homepage',
        sticky='top'
    )

    return nbar