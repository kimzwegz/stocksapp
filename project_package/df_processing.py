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


def get_dropdown_label(dashdropdown, some):
    """
    get label from dropdown menu dict value label pairs
    
    """
    for i,j in enumerate(dashdropdown):
        if j['value'] == some:
            # print(i)
            index = i
    # print(index)
    return dashdropdown[index]['label']

print('project package imported')

