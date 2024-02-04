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
