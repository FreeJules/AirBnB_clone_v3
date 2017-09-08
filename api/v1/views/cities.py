#!/usr/bin/python3
"""
Module Cities API
"""
from api.v1.views import app_views, storage, City
from flask import jsonify, abort, make_response, request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_in_state(state_id):
    """
    Retrieves the list of all City objects of a State
    ----------------------------------------------------------------------------
    curl --request GET \
    --url http://localhost:5000/api/v1/states/%3Cstate_id%3E/cities
    """
    state = storage.get("State", state_id)
    if state is not None:
        cities = [city.to_json() for city in state.cities]
    else:
        abort(404)
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def city_by_id(city_id):
    """
    Retrieves a City object by id
    ----------------------------------------------------------------------------
    curl --request GET \
    --url http://localhost:5000/api/v1/cities/%3Ccity_id%3E
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_json())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object by id
    ----------------------------------------------------------------------------
    curl --request DELETE \
    --url http://localhost:5000/api/v1/cities/%3Ccity_id%3E
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a City
    ----------------------------------------------------------------------------
    curl --request POST \
    --url http://localhost:5000/api/v1/states/%3Cstate_id%3E/cities \
    --header 'content-type: application/json' \
    --data '{"name" : "Eureka"}'
    """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    req_json = request.get_json()
    if req_json is None:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if 'name' not in req_json.keys():
        return make_response(jsonify({'error': "Missing name"}), 400)
    req_json["state_id"] = state_id
    data = City(**req_json)
    data.save()
    return jsonify(data.to_json()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """
    Updates a City
    ----------------------------------------------------------------------------
    curl --request PUT \
    --url http://localhost:5000/api/v1/cities/%3Ccity_id%3E \
    --header 'content-type: application/json' \
    --data '{"name" : "San Jose"}'
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    req_json = request.get_json()
    if req_json is None:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    for k, v in req_json.items():
        if k not in ignore_keys and hasattr(city, k):
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_json()), 200
