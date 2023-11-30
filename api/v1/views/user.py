#!/usr/bin/python3
"""API for Users"""

from tasks.users import User
from tasks import storage
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_users():
    """Retrives the list of all User objects"""
    users = storage.all(User)
    user_list = []
    for user in users:
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route('/users/by_id/<id>', methods=['GET'], strict_slashes=False)
def get_user_id(id):
    """Retrieves a user by user id"""
    users = storage.get_user_by_id(User, id)
    if not users:
        abort(404)

    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<email_address>',
                 methods=['GET'], strict_slashes=False)
def get_user_email(email_address):
    """Retrieves a user by user's email_address"""
    users = storage.get_user_by_email(User, email=email_address)
    if not users:
        abort(404)

    return jsonify([users.to_dict()])


@app_views.route('/users/<email_address>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(email_address):
    """Deletes user"""
    user = storage.get_user_by_email(User, email=email_address)
    if not user:
        abort(404)

    storage.delete(user)
    return make_response(jsonify({}), 200)


@app_views.route('/users/by_id/<id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(id):
    """Update a user"""
    users = storage.get_user_by_id(User, id=id)
    if not users:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['__class__', 'id', 'created_at', 'updated_at']

    data = request.get_json()
    for user in users:
        for key, value in data.items():
            if key not in ignore:
                setattr(user, key, value)

    storage.save()
    users = storage.get_user_by_id(User, id=id)
    for user in users:
        return make_response(jsonify(user.to_dict()), 200)


@app_views.route('/users',
                 methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new user"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'email_address' not in request.get_json():
        abort(400, description="Missing email address")
    if 'first_name' not in request.get_json():
        abort(400, description="Missing first name")
    if 'last_name' not in request.get_json():
        abort(400, description="Missing last name")

    data = request.get_json()
    new_user = User(**data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)
