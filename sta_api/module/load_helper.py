from sta_core.handler.db_handler import DataBaseHandler
from sta_core.handler.shelve_handler import ShelveHandler


global_dict = {}
def make_global(key, value):
    global global_dict
    global_dict[key] = value


def tester():
    print("test")
    return "tester"

def db_exists():
    dbh = DataBaseHandler(db_type=global_dict["db-type"])
    dbh.set_db_path(db_path=global_dict["db-path"])
    dbh.set_db_name(db_name=global_dict["db-name"])
    db_exists = dbh.get_database_exists()
    return db_exists

def get_handler():
    dbh = DataBaseHandler(db_type=global_dict["db-type"])
    dbh.set_db_path(db_path=global_dict["db-path"])
    dbh.set_db_name(db_name=global_dict["db-name"])
    return dbh

