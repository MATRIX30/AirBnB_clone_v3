#!/usr/bin/python3
"""module to handle amenity API request"""
from models.place import Place
from models.city import City
from models.user import User
from flask import request, jsonify, make_response, abort
from api.v1.views import app_views
from models import storage


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """method to get all places in a city"""
    is_valid_city = False
    for city in storage.all(City).values():
        if city_id == city.id:
            is_valid_city = True
    if not is_valid_city:
        abort(404)
    places = []
    for place in storage.all(Place).values():
        if place.city_id == city_id:
            places.append(place.to_dict())
    return jsonify(places)


@app_views.route("/places/<place_id>",
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """method to get place by id"""
    for place in storage.all(Place).values():
        if place.id == place_id:
            return jsonify(place.to_dict())
    abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """method to delete place by id"""
    for place in storage.all(Place).values():
        if place.id == place_id:
            place.delete()
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """method to create a new place"""
    is_valid_city = False
    for city in storage.all(City).values():
        if city_id == city.id:
            is_valid_city = True
    if not is_valid_city:
        abort(404)

    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, "Not a JSON")
    if 'user_id' not in request_data.keys():
        abort(400, "Missing user_id")

    is_valid_user = False
    for user in storage.all(User).values():
        if request_data.gets('user_id') == user.id:
            is_valid_user = True
    if not is_valid_user:
        abort(400, "Missing user_id")

    if 'name' not in request_data.keys():
        abort(400, "Missing name")
    list_attrib = ["name", "description", "number_rooms", "number_bathrooms",
                   "max_guest", "price_by_night", "latitude", "longitude"]
    kwargs = {attrib: value for attrib,
              value in request_data.items() if attrib in list_attrib}
    new_place = City(**kwargs)

    # new_place = Place(**request_data)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """method to update place"""
    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, "Not a JSON")
    list_attrib = ["name", "description", "number_rooms", "number_bathrooms",
                   "max_guest", "price_by_night", "latitude", "longitude"]
    for place in storage.all(Place).values():
        if place.id == place_id:
            for attrib, value in request_data.items():
                if attrib in ["id", "user_id", "city_id", "created_at",
                              "updated_at"]:
                    continue
                if attrib in list_attrib:
                    setattr(place, attrib, value)
            place.save()
            return make_response(jsonify(place.to_dict()), 200)
    abort(404)
