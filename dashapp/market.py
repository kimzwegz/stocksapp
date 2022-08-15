from dash import Dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from datetime import date

from dashapp.instance import dash_app
# from dashapp import dash_app

from os import pardir, path
import sys

# mod_path = path.abspath(path.join(pardir))
mypackage = r'/Users/karimkhalil/Coding/development'

dirs = [mypackage]
# print(dirs)

for i in dirs:
    # print(i)
    if i not in sys.path:
        sys.path.append(i)

print(sys.path)

from mypackages import DB_mongo
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
                            initial_visible_month=date(2000, 1, 1),
                            end_date=date(2022, 12, 30)
                            ),
                    dbc.Button('Submit', id="btn-idx-date", n_clicks=0)
                    ],
                    )

market = html.Div([
            html.H3(id= 'idx-symbol'),
            dcc.Dropdown(id='market-idx-dropdown', options = market_idx_dropdown),
            html.Br(),
            html.Div(id='div_date', children=[]),
            html_date,
            dcc.Graph(id = 'market-idx-graph', figure={}),
            # dcc.Graph(id = 'market-idx-graph2', figure={}),
            # dcc.DatePickerRange(
            #                     id='idx-date-picker',
            #                     min_date_allowed=date(1970, 1, 1),
            #                     max_date_allowed=date(2022, 12, 30),
            #                     initial_visible_month=date(2022, 12, 30),
            #                     end_date=date(2022, 12, 30)
            #                     ),
            html.H4(id='store-out'),
            dcc.Store(id='memory-test', data=[], storage_type='memory')
])


@dash_app.callback(
    [Output(component_id='market-idx-graph', component_property='figure'),
    Output(component_id='idx-symbol', component_property='children')],
    [State(component_id='market-idx-dropdown', component_property='value'),
    State(component_id='idx-date-picker', component_property='start_date'),
    State(component_id='idx-date-picker', component_property='end_date'),
    Input(component_id='btn-idx-date', component_property='n_clicks')],
    prevent_initial_call=True, preventupdate=True
)

def drop_down(option, start_date, end_date, n_clicks):

    if start_date is not None and end_date is not None and n_clicks is not None:
        print(option)
        df_fig = df_idx_price.loc[(df_idx_price['symbol'] == option) & df_idx_price['datetime'].between(start_date, end_date)]
        cols = [i for i in df_fig.columns if i != "_id"]
        df_fig_store = df_fig[cols]
        df_fig_store['datetime'] = df_fig_store['datetime'].dt.strftime("%Y-%m-%d")
        print(df_fig_store.info())

        dict_fig_store = df_fig_store.to_dict('records')
        for i in dict_fig_store[0]:
            print(i , dict_fig_store[0][i], type(dict_fig_store[0][i]))

        print(f'selection is {option}\n')
        fig = px.line(df_fig, x='datetime', y = 'adjClose', color='name')
        print(type(dict_fig_store))
        return fig ,option



if __name__ == '__main__':
    fig.show()