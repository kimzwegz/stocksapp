from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dashapp.tabs import navbar, main_tabs

main_layout = dbc.Container([navbar,main_tabs])

def create_dash_application(flask_app):
    dash_app = Dash(server=flask_app, name="Dashboard", url_base_pathname="/dash/", external_stylesheets=[dbc.themes.BOOTSTRAP])
    dash_app.layout = main_layout

    # for view_function in dash_app.server.view_functions:
    #     if view_function.startswith(dash_app.config.url_base_pathname):
    #         dash_app.server.view_functions[view_function] = login_required(
    #             dash_app.server.view_functions[view_function]
    #         )

    return dash_app