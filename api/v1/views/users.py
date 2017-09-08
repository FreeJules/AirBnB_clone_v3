#!/usr/bin/python3
"""
Module Users API
"""
from api.v1.views import app_views, storage, User
from flask import jsonify, abort, make_response, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """
    Retrieves the list of all User objects
    ----------------------------------------------------------------------------
    curl --request GET \
    --url http://localhost:5000/api/v1/users
    """
    users = [user.to_json() for user in storage.all("User")]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_by_id(user_id):
    """
    Retrieves a User object by id
    ----------------------------------------------------------------------------
    curl --request GET \
    --url http://localhost:5000/api/v1/users/%3Cuser_id%3E
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object by id
    ----------------------------------------------------------------------------
    curl --request DELETE \
    --url http://localhost:5000/api/v1/users/%3Cuser_id%3E
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a User
    ----------------------------------------------------------------------------
    curl --request POST \
    --url http://localhost:5000/api/v1/users/ \
    --header 'content-type: application/json' \
    --data '{
    "email"      : "lee@school.com",
    "first_name" : "Julia",
    "last_name"  : "Lee",
    "password"   : "password1234"
    }'
    """
    req_json = request.get_json()
    if req_json is None:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    if 'email' not in req_json.keys():
        return make_response(jsonify({'error': "Missing email"}), 400)
    if 'password' not in req_json.keys():
        return make_response(jsonify({'error': "Missing password"}), 400)
    data = User(**req_json)
    data.save()
    return jsonify(data.to_json()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    Updates a User
    ----------------------------------------------------------------------------
    curl --request PUT \
    --url http://localhost:5000/api/v1/users/%3Cuser_id%3E \
    --header 'content-type: application/json' \
    --data '{
    "first_name" : "Megha",
    "last_name"  : "Mohan",
    "email"      : "119@holberton.com",
    "password"   : "StrongPassword"
    }'
    """
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    req_json = request.get_json()
    if req_json is None:
        return make_response(jsonify({'error': "Not a JSON"}), 400)
    for k, v in req_json.items():
        if k not in ignore_keys and hasattr(user, k):
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_json()), 200
