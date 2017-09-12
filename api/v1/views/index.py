#!/usr/bin/python3
"""
holds the endpoints
"""
from api.v1.views import app_views, storage
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """
        
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats():
    """
        
    """
    CNC = {"Amenity": "amenities",
           "City": "cities",
           "Place": "places",
           "Review": "reviews",
           "State": "states",
           "User": "users"}
    dict = {}
    for k in CNC.keys():
        dict[CNC[k]] = storage.count(k)
    return jsonify(dict)
