#!/usr/bin/python3
"""

"""
from api.v1.views import storage, app_views, State
from flask import jsonify, make_response, request, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def viewAllStates():
    """
        
    """
    states = [[state.to_json() for state in storage.all("State").values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def viewOneState(stateId=None):
    """
        
    """
    if stateId is None:
        abort(404)
    state = storage.get("State", stateId)
    if state is None:
        abort(404)
    return jsonify(state)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def deleteState(state_id=None):
    """
        
    """
    if stateId is None:
        abort(404)
    state = storage.get("State", stateId)
    if state is None:
        abort(404)
    storage.delete(state)
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
    r.save()
    return jsonify(r), 201
