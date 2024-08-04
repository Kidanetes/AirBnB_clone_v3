#!/usr/bin/python3
"""api defintion"""


from flask import jsonify, request, abort, Request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.user import User


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """return status ok"""
    l1 = []
    dict1 = storage.all(State)
    for keys, values in dict1.items():
        l1.append(values.to_dict())
    return jsonify(l1)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_id(state_id):
    """return route /states/<state_id>"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """delete an state if the id matches the previous created states"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """create a new state"""
    try:
        request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing name")
    obj = State(name=request.json['name'])
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update an state"""
    l1 = ['id', 'created_at', 'updated_at']
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    try:
        request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    for key, values in request.json.items():
        if key not in l1:
            setattr(obj, key, values)
    storage.save()
    return jsonify(obj.to_dict()), 200
