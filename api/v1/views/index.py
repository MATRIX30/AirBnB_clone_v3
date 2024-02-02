#!/usr/bin/python3
""" implements various api routes"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """returns the status of api server"""
    api_status = {
        "status": "OK"
    }
    return jsonify(api_status)
