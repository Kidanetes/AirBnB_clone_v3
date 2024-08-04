#!/usr/bin/python3
"""this module contains implementation
of flask framework"""


from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask import Blueprint
from os import getenv
from flask_cors import CORS


app = Flask(__name__)

app.register_blueprint(app_views)
CORS(app, origins=["0.0.0.0"])


@app.teardown_appcontext
def close_connection(self):
    """close a context"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """handle 404 not found error"""
    dict1 = {"error": "Not found"}
    return jsonify(dict1), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host, port, threaded=True)
