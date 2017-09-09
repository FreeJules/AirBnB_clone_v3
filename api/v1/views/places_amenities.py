#!/usr/bin/python3
"""
Module Places Amenities API
"""
import os
from api.v1.views import app_views, storage, Place, Amenity
from flask import jsonify, abort, make_response, request
storage_type = os.environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def all_place_amenities(place_id):
    """
    Retrieves the list of all Place Amenity objects of a Place
    ----------------------------------------------------------------------------
    curl --request GET \
    --url http://localhost:5000/api/v1/places/%3Cplace_id%3E/amenities
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenities = [amenity.to_json() for amenity in place.amenities]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes a Amenity object to a Place
    ----------------------------------------------------------------------------
    curl --request DELETE \
    --url http://localhost:5000/api/v1/...
    ...places/%3C<place_id>%3E/amenities/%3C<amenity_id>%3E
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenities = place.amenities()
    if amenity.id not in amenities.keys():
        abort(404)
    if storage_type != db:
        place.amenity_ids.remove(amenity_id)
    else:
        place.amenities.remove(amenity)
    place.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """
    Links a Amenity object to a Place
    ----------------------------------------------------------------------------
    curl --request POST \
    --url http://localhost:5000/api/v1/...
    ...places/%3C<place_id>%3E/amenities/%3C<amenity_id>%3E
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
