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
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_json())


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
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    storage.delete(place)
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
        setattr(place, k, v)
    place.save()
    return jsonify(place.to_json()), 200


""" ADVANCED: places_search """


@app_views.route('/places_search',
                 methods=['POST'], strict_slashes=False)
def searchPlace():
    """
        Searches a Place object
        curl --request POST \
        --url http://localhost:5000/api/v1/places_search \
        --header 'content-type: application/json' \
        --data '{"states" : ["31599588-39d3-48bd-84e5-b929b7eaf7cd"], \
                 "cities" : ["23459588-39d3-48bd-84e5-b929b7eaf6ba"], \
                 "amenities" : ["15659588-39d3-48bd-84e5-b929b7eafcbd"] \
                }
    """
    reqJson = request.get_json()
    if reqJson is None:
        return "Not a JSON", 400
    """
    If the JSON body is empty or each list of all keys are empty:
    retrieve all Place objects
    """
    if not reqJson or (not reqJson['states'] and
                       not reqJson['cities'] and
                       not reqJson['amenities']):
        places = [place.to_json() for place in storage.all("Place").values()]
        return jsonify(places)
    """
    If states list is not empty, search for Place objects
    inside each State ids listed
    """
    places = []
    state_ids = reqJson['states']
    if not state_ids:
        st_city_ids = []
    else:
        for state_id in state_ids:
            state = storage.get("State", state_id)
            if state is not None:
                st_city_ids = [getattr(city, 'id') for city in state.cities]
    city_ids = reqJson['cities']
    if not city_ids:
        city_ids = []
    all_city_ids = list(set(st_city_ids) | set(city_ids))
    for city_id in all_city_ids:
        city = storage.get("City", city_id)
        if city is not None:
            places.extend([place for place in city.places])
    amenity_ids = reqJson['amenities']
    if amenity_ids:
        set_amenity_ids = set(amenity_ids)
        """places_copy = list(places)"""
        for place in places:
            pl_am_ids = [getattr(amenity, 'id') for amenity in place.amenities]
            set_pl_am_ids = set(pl_am_ids)
            if not set_amenity_ids.issubset(set_pl_am_ids):
                places.remove(place)
    places_to_json = [p.to_json() for p in places]
    return jsonify(places_to_json)
