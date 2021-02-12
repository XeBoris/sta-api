"""Console script for sta_api."""
import argparse
import sys
import os
import pickle
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import numpy as np

import sta_core as stacore

from .module.config import HandleConfiguration

from .module.api.v0.data import route_data
from .module.home import main_routes

import sta_api as staapi

from .module.load_helper import make_global



def main():
    """Console script for sta_api."""
    parser = argparse.ArgumentParser(
        description="The sta-api application to allow communication via RestAPI"
    )

    parser.add_argument('_', nargs='*')
    parser.add_argument('--debug', action='store_true',
                        help='Use flask server in debug mode')
    parser.add_argument('--config', dest="config", default=None)
    args = parser.parse_args()

    hc = HandleConfiguration()
    if args.config is not None:
        hc.set_path(args.config)
    else:
        p = os.path.join(staapi.__path__[0], "configuration/sta_api.config")
        hc.set_path(p)

    make_global("db-type", hc.get_sta_db_type())
    make_global("db-name", hc.get_sta_db_name())
    make_global('db-path', hc.get_sta_db_path())

    app = Flask(__name__)
    api = Api(app)  # Require a parser to parse our POST request.
    app.register_blueprint(main_routes)
    app.register_blueprint(route_data)


    #Going for the server
    flask_port = hc.get_port()
    flask_debug = hc.flask_debug()
    if flask_debug is True:
        print("Running in debug mode")
        CORS(app)
        app.run(host='0.0.0.0',
                port=flask_port,
                debug=flask_debug)
    else:
        app.run(host='0.0.0.0',
                port=flask_port,
                debug=flask_debug)



if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
