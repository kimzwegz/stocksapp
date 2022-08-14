from dash import Dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
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

market = html.Div([
            html.H3(id= 'idx-symbol'),
            dcc.Dropdown(id='market-idx-dropdown', options = market_idx_dropdown),
            html.Br(),
            html.Div(id='div_date', children=[]),
            dcc.Graph(id = 'market-idx-graph', figure={}),
            dcc.DatePickerRange(
                                id='idx-date-picker',
                                min_date_allowed=date(1995, 8, 5),
                                max_date_allowed=date(2017, 9, 19),
                                initial_visible_month=date(2017, 8, 5),
                                end_date=date(2017, 8, 25)
                                ),
            dcc.Store(id='memory-test', data=[], storage_type='memory')
])


@dash_app.callback(
    [Output(component_id='market-idx-graph', component_property='figure'),
    Output(component_id='idx-symbol', component_property='children'),
    Output(component_id='div_date', component_property='children'),
    Output(component_id='memory-test', component_property='data')],
    [Input(component_id='market-idx-dropdown', component_property='value')],
    prevent_initial_call=True
)

def drop_down(option):
    df_fig = df_idx_price.loc[df_idx_price['symbol'] == option]
    
    date_min_str = pd.to_datetime(df_fig['datetime'].idxmin()).strftime("%m/%d/%Y")
    date_max_str = pd.to_datetime(df_fig['datetime'].idxmax()).strftime("%m/%d/%Y")
    
    date_min = pd.to_datetime(df_fig['datetime'].idxmin()).strftime("%m/%d/%Y")
    date_max = pd.to_datetime(df_fig['datetime'].idxmax()).strftime("%m/%d/%Y")

    df_fig_store = df_fig[['symbol', 'name' ,'datetime', 'month' , 'year' , 'adjClose']]
    df_fig_store['datetime'] = df_fig_store['datetime'].dt.strftime("%m-%d-%Y")


    dict_fig = df_fig_store.to_dict('records')

    print(f'selection is {option} from {date_min_str} to {date_max_str}\n')
    fig = px.line(df_fig, x='datetime', y = 'adjClose', color='name')
    html_date  = dcc.DatePickerRange(
                                id='idx-date-picker2',
                                min_date_allowed=date_min,
                                max_date_allowed=date_max,
                                initial_visible_month=date_min,
                                end_date=date_max
                                )

    print(type(dict_fig))
    return fig ,option, html_date, dict_fig

if __name__ == '__main__':
    fig.show()