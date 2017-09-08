#!/usr/bin/python3
"""
    view for Place objects that handles all default RestFul API actions
"""
from api.v1.views import storage, app_views, Place
from flask import (jsonify, make_response, request, abort)
from os import getenv


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def viewAllPlaces(city_id=None):
    """
        view all places objects
        curl --request GET \
        --url http://localhost:5000/api/v1/cities/%3Ccity_id%3E/places
    """
    city = storage.get("City", city_id)
    if city is not None:
        places = [place.to_json() for place in city.places]
    else:
        abort(404)
    return jsonify(places)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def viewPlacesById(place_id=None):
    """
        Retrieves a Place object based on ID
        -------------------------------------
        curl --request GET \
        --url http://localhost:5000/api/v1/places/%3Cplace_id%3E
    """
    if place_id is None:
        abort(404)
    places = storage.get("Place", place_id)
    if places is None:
        abort(404)
    return jsonify(amenity.to_json())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def deletePlace(place_id=None):
    """
        Deletes a Place object
        curl --request DELETE \
        --url http://localhost:5000/api/v1/places/%3Cplace_id%3E
    """
    if place_id is None:
        abort(404)
    places = storage.get("Place", place_id)
    if places is None:
        abort(404)
    storage.delete(places)
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def createPlace(city_id):
    """
        Creates a Place object
        curl --request POST \
        --url http://localhost:5000/api/v1/cities/%3Ccity_id%3E/places \
        --header 'content-type: application/json' \
        --data '{"user_id" : "31599588-39d3-48bd-84e5-b929b7eaf7cd", \
        "name"    : "2907 Harrison St"}'
    """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    reqJson = request.get_json()
    if reqJson is None:
        return "Not a JSON", 400
    if "user_id" not in reqJson.keys():
        return "Missing user_id", 400
    # If the user_id is not linked to any User object, raise a 404 error
    uid_Req = reqJson.get("user_id")
    user = storage.get("User", uid_Req)
    if user is None:
        abort(404)
    # If the dictionary doesn't contain the key name, raise a 400
    if "name" not in reqJson.keys():
        return "Missing name", 400
    # add city id to the new place obj
    reqJson["city_id"] = city_id
    data = Place(**reqJson)
    data.save()
    return jsonify(data.to_json()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def updatePlace(place_id=None):
    """
        updates a Place object
        curl --request PUT \
        --url http://localhost:5000/api/v1/places/%3Cplace_id%3E \
        --header 'content-type: application/json' \
        --data '{"name" : "Bobby'\''s House"}'
    """
    reqJson = request.get_json()
    if reqJson is None:
        return "Not a JSON", 400
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    for fields in ("id", "user_id", "city_id", "created_at", "updated_at"):
        reqJson.pop(fields, None)
    for k, v in reqJson.items():
        setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_json()), 200
