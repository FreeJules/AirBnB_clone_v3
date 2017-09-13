#!/usr/bin/python3
"""
amenity objects that handles all default RestFul API actions
"""
from api.v1.views import storage, app_views, State, Amenity
from flask import (jsonify, make_response, request, abort)
from os import getenv


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def viewAllAmenities():
    """
        view all state objects
        curl --request GET \
        --url http://localhost:5000/api/v1/amenities
    """
    amenities = [amnty.to_json() for amnty in storage.all("Amenity").values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def viewOneAmenity(amenity_id=None):
    """
        Retrieves an Amenity object
        curl --request GET \
        --url http://localhost:5000/api/v1/amenities/%3Camenity_id%3E
    """
    if amenity_id is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_json())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def deleteAmenity(amenity_id=None):
    """
        Deletes Amenity object
        curl --request DELETE \
        --url http://localhost:5000/api/v1/amenities/%3Camenity_id%3E
    """
    if amenity_id is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def createAmenity():
    """
        Creates an Amenity object
        curl --request POST \
        --url http://localhost:5000/api/v1/amenities/ \
        --header 'content-type: application/json' \
        --data '{"name" : "Poop"}'
    """
    reqJson = request.get_json()
    if reqJson is None:
        return "Not a JSON", 400
    if 'name' not in reqJson.keys():
        return "Missing name", 400
    data = Amenity(**reqJson)
    data.save()
    return jsonify(data.to_json()), 201


@app_views.route('/amenities/<amenities_id>',
                 methods=['PUT'], strict_slashes=False)
def updateAmenity(amenities_id=None):
    """
        updates an Amenity object
        curl --request PUT \
        --url http://localhost:5000/api/v1/amenities/%3Camenity_id%3E \
        --header 'content-type: application/json' \
        --data '{"name" : "Toilet"}'
    """
    reqJson = request.get_json()
    if reqJson is None:
        return "Not a JSON", 400
    amenity = storage.get("Amenity", amenities_id)
    if amenity is None:
        abort(404)
    for fields in ("id", "created_at", "updated_at"):
        reqJson.pop(fields, None)
    for k, v in reqJson.items():
        setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_json()), 200
