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


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def places_in_a_city(city_id):
    """return route /states/<state_id>/cities"""
    l1 = []
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    for i in obj.places:
        l1.append(i.to_dict())
    return jsonify(l1)


@app_views.route('places/<place_id>', methods=['GET'], strict_slashes=False)
def places(place_id):
    """return route /states/<state_id>/cities"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """delete an state if the id matches the previous created states"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """create a new state"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if "user_id" not in request.json:
        abort(400, "Missing user_id")
    obj2 = storage.get(User, request.json['user_id'])
    if obj2 is None:
        abort(404)
    if "name" not in request.json:
        abort(400, "Missing name")
    new_obj = Place(name=request.json['name'],
                    user_id=request.json['user_id'], city_id=obj.id)
    storage.new(new_obj)
    storage.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update an state"""
    l1 = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for key, values in request.json.items():
        if key not in l1:
            setattr(obj, key, values)
    storage.save()
    return jsonify(obj.to_dict()), 200
