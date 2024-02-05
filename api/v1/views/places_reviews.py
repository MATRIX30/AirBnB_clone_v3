#!/usr/bin/python3
from models.review import Review
from models.place import Place
from models.user import User
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage


@app_views.route("/places/<place_id>/reviews", methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """method to get all reviews"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """method to get reviews by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """method to delete a review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """method to create new review"""
    request_data = request.get_json(silent=True)

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request_data:
        abort(400, "Not a JSON")
    if 'user_id' not in request_data:
        abort(400, "Missing user_id")
    user = storage.get(User, request_data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in request_data:
        abort(400, "Missing text")
    new_review = Review(**request_data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """method to update review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, "Not a JSON")
    for attrib, value in request_data.items():
        if attrib not in ["id", "user_id", "place_id",
                          "created_at", "updated_at"]:
            setattr(review, attrib, value)
    storage.save()
    return jsonify(review.to_dict()), 200
