from flask import Blueprint, jsonify, request, abort
import json

movies_bp = Blueprint('movies', __name__)
directors_bp = Blueprint('directors', __name__)

movies = {
    '1': {'title': 'Love and Basketball', 'director': 'Gina Prince-Bythewood', 'release_date': '2000'},
    # Assume other movies are added here...
}

@movies_bp.route('/movies', methods=['GET'])
def get_movies():
    return jsonify(list(movies.values()))

@movies_bp.route('/movies/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = movies.get(movie_id)
    if not movie:
        abort(404, description="Movie not found")
    return jsonify(movie)

@movies_bp.route('/movies', methods=['POST'])
def add_movie():
    movie_data = request.get_json()
    if not movie_data:
        abort(400, description="Invalid data")
    new_id = str(max([int(x) for x in movies.keys()]) + 1) if movies else '1'
    movies[new_id] = movie_data
    return jsonify(movies[new_id]), 201

@movies_bp.route('/movies/<movie_id>', methods=['PUT'])
def update_movie(movie_id):
    if movie_id not in movies:
        abort(404, description="Movie not found")
    movie_data = request.get_json()
    movies[movie_id].update(movie_data)
    return jsonify(movies[movie_id])

@movies_bp.route('/movies/<movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    if movie_id in movies:
        del movies[movie_id]
        return jsonify({'message': 'Movie deleted'}), 200
    abort(404, description="Movie not found")