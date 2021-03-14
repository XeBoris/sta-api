import os
import pandas as pd

from sta_core.handler.db_handler import DataBaseHandler
from sta_core.handler.shelve_handler import ShelveHandler

from sta_api.module.load_helper import global_dict
from sta_api.module.load_helper import tester
from sta_api.module.load_helper import db_exists


from flask import Blueprint, redirect, request
from flask import jsonify
from markupsafe import escape

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

@route_data.route(f'{all_route_data}/data/users/all',
                  methods=["GET"])
def all_users():
    dbh = DataBaseHandler(db_type=global_dict["db-type"])
    dbh.set_db_path(db_path=global_dict["db-path"])
    dbh.set_db_name(db_name=global_dict["db-name"])
    all_users = dbh.get_all_users(by="user_username")

    del dbh
    return jsonify(all_users)

@route_data.route(f'{all_route_data}/data/user/<username>',
                  methods=["GET"])
def get_user(username):
    user_name = escape(username)

    dbh = DataBaseHandler(db_type=global_dict["db-type"])
    dbh.set_db_path(db_path=global_dict["db-path"])
    dbh.set_db_name(db_name=global_dict["db-name"])

    all_users = dbh.get_all_users(by="user_username")

    if user_name in all_users:
        user_entry = dbh.search_user(user=user_name, by="username")
    else:
        user_entry = []

    del dbh

    return jsonify(user_entry)

@route_data.route(f'{all_route_data}/data/branches',
                  methods=['GET'])
def get_branches():
    user_name = request.args.get('username')

    dbh = DataBaseHandler(db_type=global_dict["db-type"])
    dbh.set_db_path(db_path=global_dict["db-path"])
    dbh.set_db_name(db_name=global_dict["db-name"])
    all_users = dbh.get_all_users(by="user_username")

    user_entry = dbh.search_user(user=user_name, by="username")
    user_hash = user_entry[0].get("user_hash")

    user_tracks = dbh.read_branch(key="user_hash", attribute=user_hash)

    df = pd.DataFrame(user_tracks)

    df["start_time"] = pd.to_datetime(df["start_time"], unit="ms")
    df["end_time"] = pd.to_datetime(df["end_time"], unit="ms")
    df["created_at"] = pd.to_datetime(df["created_at"], unit="ms")
    df["updated_at"] = pd.to_datetime(df["updated_at"], unit="ms")
    df = df.sort_values(by="start_time", ascending=False)

    csvdf = df.to_json()

    return jsonify(csvdf)

@route_data.route(f'{all_route_data}/data/branch/<branch_hash>/leafs',
                  methods=['GET'])
def get_leaf(branch_hash):
    user_name = request.args.get('username')
    branch_hash = escape(branch_hash)
    #leaf_hash = escape(leaf_hash)

    print(user_name, branch_hash)

    dbh = DataBaseHandler(db_type=global_dict["db-type"])
    dbh.set_db_path(db_path=global_dict["db-path"])
    dbh.set_db_name(db_name=global_dict["db-name"])
    all_users = dbh.get_all_users(by="user_username")

    user_entry = dbh.search_user(user=user_name, by="username")
    user_hash = user_entry[0].get("user_hash")

    user_tracks = dbh.read_branch(key="user_hash", attribute=user_hash)

    df = pd.DataFrame(user_tracks)
    df = df[df["track_hash"] == branch_hash]

    leaf_names = [k.get("name") for i, k in df["leaf"].iloc[0].items()]
    leaf_hashes = [k.get("leaf_hash") for i, k in df["leaf"].iloc[0].items()]

    ret_dict = {}
    for i in range(len(leaf_names)):
        leaf_name = leaf_names[i]
        leaf_content = leaf_hashes[i]
        df_i = dbh.read_leaf(directory=leaf_name,
                         leaf_hash=leaf_content,
                         leaf_type="DataFrame")

        print(df_i.head(3))

        ret_dict[leaf_name] =  csvdf = df_i.to_json()



    return ret_dict
