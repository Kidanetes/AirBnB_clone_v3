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


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """return status ok"""
    l1 = []
    dict1 = storage.all(Amenity)
    for keys, values in dict1.items():
        l1.append(values.to_dict())
    return jsonify(l1)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenitys_id(amenity_id):
    """return route /amenities/<amenity_id>"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete an state if the id matches the previous created states"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """create a new state"""
    try:
        request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing name")
    obj = Amenity(name=request.json['name'])
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """update an state"""
    l1 = ['id', 'created_at', 'updated_at']
    obj = storage.get(Amenity, amenity_id)
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
