# app/routes/movies.py
from flask import Blueprint, jsonify, request

movies_bp = Blueprint('movies', __name__)

# Assuming a simple 'movies' dictionary
movies = {
    '1': {'title': 'Love and Basketball', 'director': 'Gina Prince-Bythewood', 'release_date': '2000'},
    '2': {'title': "What's Love Got to Do with It", 'director': 'Brian Gibson', 'release_date': '1993'},
    '3': {'title': 'The Color Purple', 'director': 'Steven Spielberg', 'release_date': '1985'}
}

@movies_bp.route('/movies', methods=['GET'])
def get_movies():
    return jsonify(list(movies.values()))

@movies_bp.route('/movies', methods=['POST'])
def add_movie():
    movie_data = request.get_json()
    movie_id = str(len(movies) + 1)
    movies[movie_id] = movie_data
    return jsonify(movies[movie_id]), 201

@movies_bp.route('/movies/<movie_id>', methods=['GET', 'PUT', 'DELETE'])
def movie(movie_id):
    if request.method == 'GET':
        return jsonify(movies.get(movie_id, {'message': 'Movie not found'}))
    elif request.method == 'PUT':
        movies[movie_id].update(request.get_json())
        return jsonify(movies[movie_id])
    elif request.method == 'DELETE':
        if movie_id in movies:
            del movies[movie_id]
            return jsonify({'message': 'Movie deleted'})
        return jsonify({'message': 'Movie not found'})