#!/usr/bin/python3
"""
view for State objects that handles all default RestFul API actions
"""
from api.v1.views import storage, app_views, State
from flask import (jsonify, make_response, request, abort)
from os import getenv


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def viewAllStates():
    """
        
    """
    states = [state.to_json() for state in storage.all("State").values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def viewOneState(state_id=None):
    """
        
    """
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    print(state)
    return jsonify(state.to_json())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def deleteState(state_id=None):
    """
        
    """
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    print(state)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    storage.reload()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def createState():
    """
        
    """
    reqJson = request.get_json()
    if reqJson is None:
        return "Not a JSON", 400
    if 'name' not in reqJson.keys():
        return "Missing name", 400
    data = State(**reqJson)
    data.save()
    return jsonify(data.to_json()), 201


@app_views.route('/states/<states_id>', methods=['PUT'], strict_slashes=False)
def updateState():
    """
        
    """
    

