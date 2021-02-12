import os
import pandas as pd

from sta_core.handler.db_handler import DataBaseHandler
from sta_core.handler.shelve_handler import ShelveHandler

from sta_api.module.load_helper import global_dict
from sta_api.module.load_helper import tester
from sta_api.module.load_helper import db_exists


from flask import Blueprint, redirect, request
route_data = Blueprint('data', __name__,)

all_route_data = "/api/v0"




def data_f():
    k = {"a": [1,2,3,4,5,6,7,8],
         "b": [1,2,3,4,5,6,7,8]}
    df = pd.DataFrame(k)
    return df

@route_data.route(f'{all_route_data}/data')
def data():
    df = data_f()
    print(df.head(3))
    df_json = df.to_json()
    print(df_json)
    print(tester())
    print( db_exists() )
    return df_json
    #return "Welcome to strava-data "

@route_data.route(f'{all_route_data}/data/user/all',
                  methods=["GET"])
def all_users():
    dbh = DataBaseHandler(db_type=global_dict["db-type"])
    dbh.set_db_path(db_path=global_dict["db-path"])
    dbh.set_db_name(db_name=global_dict["db-name"])
    all_users = dbh.get_all_users(by="user_username")
    print(all_users)
    del dbh
    return "0"
