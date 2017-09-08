#!/usr/bin/python3
"""
handles all default RestFul API actions
"""
from api.v1.views import app_views, storage
from flask import jsonify, abort


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_in_state(state_id):
    """
    Retrieves the list of all City objects of a State
    """
    state = storage.get("State", state_id)
    if state is not None:
        cities = [city.to_json() for city in state.cities]
    return jsonify(cities)
