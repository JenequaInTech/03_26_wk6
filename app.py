from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    director = db.Column(db.String())
    release_year = db.Column(db.Integer)

    def __repr__(self):
        return f'<Movie {self.title}>'

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return "Connected to the database!"

@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify({'movies': [{'id': movie.id, 'title': movie.title, 'director': movie.director, 'release_year': movie.release_year} for movie in movies]})

@app.route('/movies', methods=['POST'])
def add_movie():
    if not request.json or not 'title' in request.json:
        abort(400)
    movie = Movie(
        title=request.json['title'],
        director=request.json.get('director', ''),
        release_year=request.json.get('release_year')
    )
    db.session.add(movie)
    db.session.commit()
    return jsonify({'id': movie.id, 'title': movie.title}), 201

@app.route('/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        abort(404)
    if not request.json:
        abort(400)
    movie.title = request.json.get('title', movie.title)
    movie.director = request.json.get('director', movie.director)
    movie.release_year = request.json.get('release_year', movie.release_year)
    db.session.commit()
    return jsonify({'id': movie.id, 'title': movie.title})

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        abort(404)
    db.session.delete(movie)
    db.session.commit()
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)