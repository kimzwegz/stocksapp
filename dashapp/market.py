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

market = html.Div([
            html.H3(id= 'idx-symbol'),
            dcc.Dropdown(id='market-idx-dropdown', options = market_idx_dropdown),
            html.Br(),
            html.Div(id='div_date', children=[]),
            dcc.Graph(id = 'market-idx-graph', figure={}),
            dcc.Graph(id = 'market-idx-graph2', figure={}),
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

html_date  = dbc.Row([dbc.Col(dcc.DatePickerRange(
                            id='idx-date-picker',
                            min_date_allowed=date(1970, 1, 1),
                            max_date_allowed=date(2022, 12, 30),
                            initial_visible_month=date(2022, 12, 30),
                            end_date=date(2022, 12, 30)
                            )),
                    dbc.Col(dbc.Button('Submit', id="btn-idx-date", n_clicks=0))
                    ],
                    )

@dash_app.callback(
    [Output(component_id='market-idx-graph', component_property='figure'),
    Output(component_id='idx-symbol', component_property='children'),
    Output(component_id='div_date', component_property='children'),
    Output(component_id='memory-test', component_property='data')],
    [Input(component_id='market-idx-dropdown', component_property='value')],
    prevent_initial_call=True, preventupdate=True
)

def drop_down(option):
    df_fig = df_idx_price.loc[df_idx_price['symbol'] == option]

    # cols = ['symbol', 'name' ,'datetime', 'month' , 'year' , 'adjClose']
    # df_fig_store['datetime'] = df_fig_store['datetime'].dt.strftime("%m-%d-%Y")
    cols = [i for i in df_fig.columns if i != "_id"]
    df_fig_store = df_fig[cols]
    df_fig_store['datetime'] = df_fig_store['datetime'].dt.strftime("%Y-%m-%d")
    print(df_fig_store.info())

    dict_fig = df_fig_store.to_dict('records')
    for i in dict_fig[0]:
        print(i , dict_fig[0][i], type(dict_fig[0][i]))

    print(f'selection is {option}\n')
    fig = px.line(df_fig, x='datetime', y = 'adjClose', color='name')

    print(type(dict_fig))
    return fig ,option, html_date, dict_fig

@dash_app.callback(
    Output(component_id='market-idx-graph2', component_property='figure'),
    [State(component_id='idx-date-picker', component_property='start_date'),
    State(component_id='idx-date-picker', component_property='end_date'),
    State(component_id='memory-test', component_property='data'),
    Input(component_id='btn-idx-date', component_property='n_clicks')],
    prevent_initial_call=True, preventupdate=True)

def store(start_date, end_date, data, n_clicks):
    # for i in data[0]:
    #     print(i , data[0][i], type(data[0][i]))
    if start_date is not None and end_date is not None and n_clicks is not None:
        df = pd.DataFrame(data)
        df['datetime'] = pd.to_datetime(df['datetime'])
        df_fig = df.loc[df['datetime'].between(start_date, end_date)]

        fig = px.line(df_fig, x='datetime', y = 'adjClose', color='name')
        print(df_fig.info())
        shape = df_fig.shape
        output = [f'{shape[0]} rows & {shape[1]} columns found- start {start_date} {end_date}']
        print(output, f"Clicked {n_clicks} times.")
        print(start_date, type(start_date), end_date, type(end_date))
        # fig.show()
    else:
        fig = px.line(None)

    return fig
        # return ['no selection']
    # df = pd.DataFrame(data)
    # shape = df.shape


if __name__ == '__main__':
    fig.show()