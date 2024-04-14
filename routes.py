# routes.py
from flask import Blueprint, jsonify, request

movies_bp = Blueprint('movies', __name__)
directors_bp = Blueprint('directors', __name__)

movies = {
    '1': {'title': 'Love and Basketball', 'director': 'Gina Prince-Bythewood', 'release_date': '2000'},
    # ... other movies
}

directors = {
    '1': {'name': 'Spike Lee', 'nationality': 'American', 'years_active': '1977-present'},
    # ... other directors
}

@movies_bp.route('/movies', methods=['GET'])
def get_movies():
    return jsonify(movies)

@movies_bp.route('/movies', methods=['POST'])
def add_movie():
    movie_data = request.get_json()
    # ... logic to add a movie
    return jsonify(movie_data), 201

# ... Other movie routes

@directors_bp.route('/directors', methods=['GET'])
def get_directors():
    return jsonify(directors)

# ... Other director routes

def configure_routes(app):
    app.register_blueprint(movies_bp)
    app.register_blueprint(directors_bp)