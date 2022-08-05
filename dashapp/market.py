from dash import Dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

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

market = html.Div([
            html.H3('Global Indexes'),
            dcc.Dropdown(id='market-idx-dropdown', options = market_idx_dropdown),
            dcc.Graph(id = 'market-idx-graph', figure={})
            ])

@dash_app.callback(
    Output(component_id='market-idx-graph', component_property='figure'),
    Input(component_id='market-idx-dropdown', component_property='value'),
    prevent_initial_call=False
)

def drop_down(option):
    df_fig = df_idx_price.loc[df_idx_price['symbol'] == option]
    fig = px.line(df_fig, x='datetime', y = 'adjClose', color='name')
    print(option)
    return fig

if __name__ == '__main__':
    fig.show()