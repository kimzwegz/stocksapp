from dash import Dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from flaskapp import app
# from dashapp.market import market




df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

#####################################################################################
#################################### EXAMPLES #######################################
#####################################################################################

# main_tabs_example = html.Div([dbc.Row([
#         dbc.Col(html.Div("WWE"), width=6),
#         dbc.Col(dbc.Button("Primary", color="primary", className="me-1", href='/', external_link=True))]),
#         dcc.Tabs(id="main_tabs", value="tab_patent", children=
#         [
#             dcc.Tab(label='Stocks', value= 'tab-1'),
#             dcc.Tab(label='Indexes', value= 'tab-2')
#             ])
#         ])

# test = html.Div(children=[
#     html.H1(children='Hello Dash'),

#     html.Div(children='''
#         Dash: A web application framework for your data.
#     '''),
#     dcc.Link(html.Button("LOG_VIEW"), href="/", refresh=True),

#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     )
# ])

#####################################################################################
#####################################################################################
#####################################################################################


main_tabs = html.Div([
    dcc.Tabs(id="main_tabs", value="tab_patent", children=[
        dcc.Tab(label='Stocks', value= 'tab-1'),
        dcc.Tab(label='Indexes', value= 'tab-2')
    ])
])


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/", external_link=True)),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 2", href="#"),
                dbc.DropdownMenuItem("Page 3", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="Stocks",
    # brand_href="#",
    color="primary",
    dark=True
)

# @app.callback(
#     Output('tabs-content', 'children'),
#     Input('main_tabs', 'value'))

# def render_tab(tab):
#     if tab == 'tab-1':
#         return market
#     if tab == 'tab-2':
#         pass