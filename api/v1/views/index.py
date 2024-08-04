#!/usr/bin/python3
"""api defintion"""


from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """return status ok"""
    return jsonify(status='OK')


@app_views.route('/stats', strict_slashes=False)
def stats():
    """return the count of  objects"""
    count = {'states': 0, 'cities': 0,
             'places': 0, 'users': 0,
             'amenities': 0, 'reviews': 0}
    class_ = {'states': State, 'cities': City,
              'places': Place, 'users': User,
              'amenities':  Amenity, 'reviews': Review}
    for i in class_:
        count[i] = storage.count(class_[i])
    return jsonify(count)
