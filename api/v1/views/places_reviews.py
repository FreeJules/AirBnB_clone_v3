#!/usr/bin/python3
"""
Module Reviews API
"""
from api.v1.views import app_views, storage, Review, Place, User
from flask import jsonify, abort, make_response, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """
    Retrieves the list of all Review objects
    ----------------------------------------------------------------------------
    curl --request GET \
    --url http://localhost:5000/api/v1/places/%3Cplace_id%3E/reviews
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    reviews = [review.to_json() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_by_id(review_id):
    """
    Retrieves a Review object by id
    ----------------------------------------------------------------------------
    curl --request GET \
    --url http://localhost:5000/api/v1/reviews/%3Creview_id%3E
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_json())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object by id
    ----------------------------------------------------------------------------
    curl --request DELETE \
    --url http://localhost:5000/api/v1/reviews/%3Creview_id%3E
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates a Review
    ----------------------------------------------------------------------------
    curl --request POST \
    --url http://localhost:5000/api/v1/places/%3Cplace_id%3E/reviews \
    --header 'content-type: application/json' \
    --data '{
    "user_id" : "9e7b2555-3bff-4569-9291-8ff875e7a6ac",
    "text"    : "Awesome place!"
    }'
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    req_json = request.get_json()
    if req_json is None:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if 'user_id' not in req_json.keys():
        return make_response(jsonify({'error': "Missing user_id"}), 400)
    uid = req_json.get("user_id")
    user = storage.get("User", uid)
    if user is None:
        abort(404)
    if 'text' not in req_json.keys():
        return make_response(jsonify({'error': "Missing text"}), 400)
    req_json["place_id"] = place_id
    data = Review(**req_json)
    data.save()
    return jsonify(data.to_json()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review
    ----------------------------------------------------------------------------
    curl --request PUT \
    --url http://localhost:5000/api/v1/reviews/%3Creview_id%3E \
    --header 'content-type: application/json' \
    --data '{
    "text" : "And great location"
    }'
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    req_json = request.get_json()
    if req_json is None:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    for k, v in req_json.items():
        if k not in ignore_keys and hasattr(review, k):
            setattr(review, k, v)
    review.save()
    return jsonify(review.to_json()), 200
