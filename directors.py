# app/routes/directors.py
from flask import Blueprint, jsonify, request, abort
import uuid

directors_bp = Blueprint('directors', __name__)

# Using a dictionary as a simple in-memory 'database' for directors
directors = {}

@directors_bp.route('/directors', methods=['GET'])
def get_directors():
    # Return all directors in JSON format
    return jsonify(list(directors.values()))

@directors_bp.route('/directors', methods=['POST'])
def add_director():
    director_data = request.get_json()
    if not director_data or 'name' not in director_data or 'years_active' not in director_data:
        abort(400, description="Missing required director fields: name and years active.")

    # Generate a unique ID for the new director using uuid4
    director_id = str(uuid.uuid4())
    directors[director_id] = {
        'id': director_id,
        **director_data
    }
    return jsonify(directors[director_id]), 201

@directors_bp.route('/directors/<director_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_director(director_id):
    if request.method == 'GET':
        # Return the director if found, else 404
        if director_id in directors:
            return jsonify(directors[director_id])
        else:
            abort(404, description="Director not found")

    elif request.method == 'PUT':
        if director_id not in directors:
            abort(404, description="Director not found")

        update_data = request.get_json()
        if not update_data:
            abort(400, description="No data provided.")

        # Update only the fields provided in the request
        for key in ['name', 'years_active']:
            if key in update_data:
                directors[director_id][key] = update_data[key]

        return jsonify(directors[director_id])

    elif request.method == 'DELETE':
        if director_id in directors:
            del directors[director_id]
            return jsonify({'message': 'Director deleted'}), 200
        else:
            abort(404, description="Director not found")