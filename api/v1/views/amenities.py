#!/usr/bin/python3
"""module to handle amenity API request"""
from models.amenity import Amenity
from flask import request, jsonify, make_response
from api.v1.views import app_views
from models import storage


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_amenities():
    """method to get all amenities"""
    amenities = []
    for amenity in storage.all(Amenity).values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>",
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """method to get amenity by id"""
    for amenity in storage.all(Amenity).values():
        if amenity.id == amenity_id:
            return jsonify(amenity.to_dict())
    abort(404)
