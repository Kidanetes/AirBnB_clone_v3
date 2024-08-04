#!/usr/bin/python3
"""api defintion"""


from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """return status ok"""
    l1 = []
    dict1 = storage.all(User)
    for keys, values in dict1.items():
        l1.append(values.to_dict())
    return jsonify(l1)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def users_id(user_id):
    """return route /users/<user_id>"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """delete an state if the id matches the previous created states"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """create a new user"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if "email" not in request.json:
        abort(400, "Missing email")
    if "password" not in request.json:
        abort(400, "Missing password")
    obj = User(**request.json)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """update a user"""
    l1 = ['id', 'email', 'created_at', 'updated_at']
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for key, values in request.json.items():
        if key not in l1:
            setattr(obj, key, values)
    storage.save()
    return jsonify(obj.to_dict()), 200
