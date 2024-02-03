#!/usr/bin/python3
"""handles api reqeust to states"""
from flask import jsonify, abort, make_response, request
from models.state import State
from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import BadRequest


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    """method to get all states"""
    states = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    for state in storage.all(State).values():
        if state.id == state_id:
            return jsonify(state.to_dict())
    abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ deletes a state by id if it exist else raise 404"""
    state_to_delete = None
    for state in storage.all(State).values():
        if state.id == state_id:
            state_to_delete = state

    if state_to_delete:
        state_to_delete.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    '''Creates a State'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    states = []
    new_state = State(name=request.json['name'])
    storage.new(new_state)
    storage.save()
    states.append(new_state.to_dict())
    return jsonify(states[0]), 201


def updates_state(state_id):
    '''Updates a State object'''
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    state_obj[0]['name'] = request.json['name']
    for obj in all_states:
        if obj.id == state_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(state_obj[0]), 200
