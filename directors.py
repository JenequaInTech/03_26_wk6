# app/routes/directors.py
from flask import Blueprint, jsonify, request

directors_bp = Blueprint('directors', __name__)

# Simple in-memory 'database' for directors
directors = {}

@directors_bp.route('/directors', methods=['GET'])
def get_directors():
    return jsonify(list(directors.values()))

@directors_bp.route('/directors', methods=['POST'])
def add_director():
    director_data = request.get_json()
    director_id = str(len(directors) + 1)
    directors[director_id] = director_data
    return jsonify(directors[director_id]), 201

@directors_bp.route('/directors/<director_id>', methods=['GET', 'PUT', 'DELETE'])
def director(director_id):
    if request.method == 'GET':
        return jsonify(directors.get(director_id, {'message': 'Director not found'}))
    elif request.method == 'PUT':
        directors[director_id].update(request.get_json())
        return jsonify(directors[director_id])
    elif request.method == 'DELETE':
        if director_id in directors:
            del directors[director_id]
            return jsonify({'message': 'Director deleted'})
        return jsonify({'message': 'Director not found'})
    