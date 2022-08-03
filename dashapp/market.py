from dash import Dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

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

df_idx_all = mongo_stock.get_df(mongo_stock.db.idx_all)
df_idx_price = mongo_stock.get_df(mongo_stock.db.idx_price)
df_idx_price = df_idx_price.merge(df_idx_all[['symbol', 'name']])
idx_sym = mongo_stock.get_unique(mongo_stock.db.idx_price, 'symbol')
# idx_sym = mongo_stock.db.idx_price.distinct('symbol')
df_idx_info = df_idx_all.loc[df_idx_all['symbol'].isin(idx_sym), ['symbol', 'name']]
fig = px.line(df_idx_price, x='datetime', y = 'adjClose', color='name')



# fig.show()
market = html.Div(fig)
if __name__ == '__main__':
    fig.show()