from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

# Configure the SQLAlchemy part of the app
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Movie model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    director = db.Column(db.String(255))
    release_year = db.Column(db.Integer)

    def __repr__(self):
        return f'<Movie {self.title}>'

# Create database tables before the first request is processed
@app.before_first_request
def create_tables():
    db.create_all()

# Route to check database connectivity
@app.route('/')
def index():
    return "Connected to the database!"

# Retrieve all movies
@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify({'movies': [{'id': movie.id, 'title': movie.title, 'director': movie.director, 'release_year': movie.release_year} for movie in movies]})

# Add a new movie
@app.route('/movies', methods=['POST'])
def add_movie():
    required_fields = ['title', 'director', 'release_year']
    if not request.json or not all(field in request.json for field in required_fields):
        abort(400, description="Missing required fields in request data")

    try:
        movie = Movie(
            title=request.json['title'],
            director=request.json.get('director', ''),
            release_year=int(request.json['release_year'])
        )
        db.session.add(movie)
        db.session.commit()
        return jsonify({'id': movie.id, 'title': movie.title}), 201

    except ValueError as e:
        abort(400, description=str(e))
    except Exception as e:
        abort(500, description="An error occurred while saving the movie")

# Update an existing movie
@app.route('/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        abort(404, description="Movie not found")
    if not request.json:
        abort(400, description="Invalid request")

    movie.title = request.json.get('title', movie.title)
    movie.director = request.json.get('director', movie.director)
    movie.release_year = request.json.get('release_year', movie.release_year)
    db.session.commit()
    return jsonify({'id': movie.id, 'title': movie.title})

# Delete a movie
@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        abort(404, description="Movie not found")
    db.session.delete(movie)
    db.session.commit()
    return jsonify({'result': True})

# Custom error handler for Forbidden access
@app.errorhandler(403)
def forbidden(error):
    return jsonify({'message': 'Forbidden access', 'error': str(error)}), 403

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)