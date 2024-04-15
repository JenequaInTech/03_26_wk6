from flask.views import MethodView
from from flask_smorest import Blueprint, abort
from flask.views import MethodView
from .schemas import MovieSchema
import uuid

# In-memory 'database' for simplicity
movies = {}

blp = Blueprint('movies', 'movies', url_prefix='/movies', description='Operations on movies')

@blp.route('/')
class Movies(MethodView):

    @blp.response(200, MovieSchema(many=True))
    def get(self):
        """Retrieve all movies"""
        return list(movies.values())

    @blp.arguments(MovieSchema)
    @blp.response(201, MovieSchema)
    def post(self, new_data):
        """Add a new movie"""
        movie_id = str(uuid.uuid4())  # Generate a unique ID for the movie
        movies[movie_id] = {**new_data, "id": movie_id}
        return movies[movie_id]

@blp.route('/<movie_id>')
class Movie(MethodView):

    @blp.response(200, MovieSchema)
    def get(self, movie_id):
        """Retrieve a specific movie"""
        movie = movies.get(movie_id)
        if not movie:
            abort(404, message="Movie not found")
        return movie

    @blp.arguments(MovieSchema)
    @blp.response(200, MovieSchema)
    def put(self, updated_data, movie_id):
        """Update an existing movie"""
        if movie_id not in movies:
            abort(404, message="Movie not found")
        movies[movie_id].update(updated_data)
        return movies[movie_id]

    @blp.response(204)
    def delete(self, movie_id):
        """Delete a movie"""
        if movie_id in movies:
            del movies[movie_id]
            return '', 204
        abort(404, message="Movie not found")