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


@app_views.route('places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def review_of_a_place(place_id):
    """return route /states/<state_id>/cities"""
    l1 = []
    obj = storage.get(Place,  place_id)
    if obj is None:
        abort(404)
    for i in obj.reviews:
        l1.append(i.to_dict())
    return jsonify(l1)


@app_views.route('reviews/<review_id>', methods=['GET'], strict_slashes=False)
def reviews(review_id):
    """return route /states/<state_id>/cities"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """delete an state if the id matches the previous created states"""
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """create a new state"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if "user_id" not in request.json:
        abort(400, "Missing user_id")
    obj2 = storage.get(User, request.json['user_id'])
    if obj2 is None:
        abort(404)
    if "text" not in request.json:
        abort(400, "Missing text")
    new_obj = Review(place_id=obj.id, **request.json)
    storage.new(new_obj)
    storage.save()
    return jsonify(new_obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """update an state"""
    l1 = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    obj = storage.get(Review, review_id)
    if obj is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for key, values in request.json.items():
        if key not in l1:
            setattr(obj, key, values)
    storage.save()
    return jsonify(obj.to_dict()), 200
