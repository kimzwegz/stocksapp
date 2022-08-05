from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from flask import Flask

def create_dash_application(flask_app):
    dash_app = Dash(server=flask_app, name="Dashboard", url_base_pathname="/dash/", external_stylesheets=[dbc.themes.BOOTSTRAP])
    dash_app.layout = main_layout

    # for view_function in dash_app.server.view_functions:
    #     if view_function.startswith(dash_app.config.url_base_pathname):
    #         dash_app.server.view_functions[view_function] = login_required(
    #             dash_app.server.view_functions[view_function]
    #         )

    return dash_app

app = Flask(__name__, template_folder=r'/Users/karimkhalil/Coding/development/stocksapp/flaskapp/templates', static_folder=r'/Users/karimkhalil/Coding/development/stocksapp/flaskapp/static')
# dash_app = Dash(name="Dashboard", external_stylesheets=[dbc.themes.BOOTSTRAP]) # for this file only
dash_app = Dash(server=app, name="Dashboard", url_base_pathname="/dash/", external_stylesheets=[dbc.themes.BOOTSTRAP]) # for main app