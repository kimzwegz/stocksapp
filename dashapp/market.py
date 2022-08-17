from dash import Dash, dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output, State
from datetime import date

from dashapp.instance import dash_app
# from dashapp import dash_app

from os import pardir, path, getcwd
import sys

# mod_path = path.abspath(path.join(pardir))
mypackage = r'/Users/karimkhalil/Coding/development'
pack_project = path.abspath(path.join(getcwd(), pardir))
dirs = [mypackage,pack_project]
# print(dirs)

for i in dirs:
    # print(i)
    if i not in sys.path:
        sys.path.append(i)

print(sys.path)

from mypackages import DB_mongo
from project_package import get_dropdown_label
from pymongo import MongoClient, ASCENDING , DESCENDING
import pandas as pd

stock = DB_mongo._CLIENT.db_fin
mongo_stock = DB_mongo(stock)
mongo_stock.db.tables

print('getting all index data from mongodb')
df_idx_all = mongo_stock.get_df(mongo_stock.db.idx_all)
cols = [i for i in df_idx_all.columns if i != '_id']
df_idx_all = df_idx_all.loc[:,cols]
df_idx_price = mongo_stock.get_df(mongo_stock.db.idx_price)
df_idx_price = df_idx_price.merge(df_idx_all[['symbol', 'name']])
idx_sym = mongo_stock.get_unique(mongo_stock.db.idx_price, 'symbol')
# idx_sym = mongo_stock.db.idx_price.distinct('symbol')
df_idx = df_idx_all.loc[df_idx_all['symbol'].isin(idx_sym), ['symbol', 'name' , 'currency', 'stockExchange']]
df_idx[['symbol', 'name']].to_dict('records')
market_idx_dropdown = [{'label': i['name'], 'value': i['symbol']} for i in df_idx[['symbol', 'name']].to_dict('records') ]   
df_idx_info = df_idx_all.loc[df_idx_all['symbol'].isin(idx_sym), ['symbol', 'name']]
fig = px.line(df_idx_price, x='datetime', y = 'adjClose', color='name')

print('figure rendered')


# fig.show()
html_date  = html.Div([dcc.DatePickerRange(
                            id='idx-date-picker',
                            min_date_allowed=date(1970, 1, 1),
                            max_date_allowed=date(2022, 12, 30),
                            initial_visible_month=date(1970, 1, 1),
                            start_date=date(1970, 1, 1),
                            end_date=date(2022, 12, 30)
                            ),
                    dbc.Button('Submit', id="btn-idx-date", n_clicks=0, style={"margin": "10px" })
                    ],
                    )
tbl_idx_info = dash_table.DataTable(id='tbl-idx-info',
                                 columns=[{"name": "item", "id": "item"},{"name": "value", "id": "value"}],
                                 data=[],
                                 style_header = {'display': 'none'},
                                 style_data = {'whiteSpace': 'normal',
                                               'height': 'auto',
                                               'lineHeight': '15px',
                                               'border': 'none',
                                            #    'backgroundColor': '#272b30',
                                            #    'color': 'white'
#                                                'textAlign': 'center'
                                              },
                                style_cell_conditional=[
                                    {'if': {'column_id': 'item'},
                                     'width': '40%',
                                     'textAlign': 'left',
                                     'fontWeight' : 'bold'
# #                                      'backgroundColor': 'rgba(0, 116, 217, 0.3)',
# #                                      'color': 'rgba(0,20,80,1)'
                                    }]
                                    )

market = html.Div([
            dbc.Row([
                dcc.Dropdown(id='market-idx-dropdown', options = market_idx_dropdown)
            ]),
            html.Br(),
            dbc.Row([
                dbc.Col(
                        [
                        html_date,
                        dcc.Graph(id = 'market-idx-graph', figure={})
                        ], width={'size': 9, 'offset': 0, 'order': 1}), 
                dbc.Col(tbl_idx_info, width={'size': 3, 'offset': 0, 'order': 2}), html.Hr()]),
            html.H4(id='store-out'),
            dcc.Store(id='memory-test', data=[], storage_type='memory')
            ]),


@dash_app.callback(
    [Output(component_id='market-idx-graph', component_property='figure'),
    Output(component_id='tbl-idx-info', component_property='data'),
    Output(component_id='tbl-idx-info', component_property='columns')],
    [State(component_id='market-idx-dropdown', component_property='value'),
    State(component_id='idx-date-picker', component_property='start_date'),
    State(component_id='idx-date-picker', component_property='end_date'),
    Input(component_id='btn-idx-date', component_property='n_clicks')],
    prevent_initial_call=True, preventupdate=True
)

def drop_down(option, start_date, end_date, n_clicks):

    if start_date is not None and end_date is not None and n_clicks is not None:

        option_label = get_dropdown_label(market_idx_dropdown, option)
        print(f'selection is {option}-{option_label}\n')

        df_fig = df_idx_price.loc[(df_idx_price['symbol'] == option) & df_idx_price['datetime'].between(start_date, end_date)]
        cols = [i for i in df_fig.columns if i != "_id"]
        df_fig_store = df_fig[cols]
        df_fig_store['datetime'] = df_fig_store['datetime'].dt.strftime("%Y-%m-%d")
        # print(df_fig_store.info())

        ################## index info ######################
        df_idx_option = df_idx[df_idx['symbol']==option]
        df_idx_option.columns= ['Symbol', 'Name', 'Currency', 'Stock Exchange']
        df_idx_option = df_idx_option.transpose().reset_index()
        df_idx_option.columns = ["item", "value"]
        col_idx_option = [{"name": i, "id": i} for i in df_idx_option.columns]
        dict_idx_option = df_idx_option.to_dict('records')
        print(dict_idx_option)
        #####################################################

        fig = plot = go.Figure(go.Scatter(x=df_fig['datetime'], y = df_fig['adjClose']))
        fig.update_layout(
            height=600,
            title_text=f"Time series for {option_label}",
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="YTD",
                            step="year",
                            stepmode="todate"),
                        dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                        dict(count=5,
                            label="5y",
                            step="year",
                            stepmode="backward"),
                        dict(count=10,
                            label="10y",
                            step="year",
                            stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )
        # print(type(dict_fig_store))
        return fig, dict_idx_option, col_idx_option



if __name__ == '__main__':
    fig.show()