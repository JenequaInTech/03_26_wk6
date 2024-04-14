from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import MovieSchema

blp = Blueprint('movies', 'movies', description='Operations on movies')

# Example in-memory database
movies = [
    {'id': 1, 'title': 'Love and Basketball', 'director': 'Gina Prince-Bythewood', 'release_year': 2000},
    {'id': 2, 'title': "What's Love Got to Do with It", 'director': 'Brian Gibson', 'release_year': 1993},
    {'id': 3, 'title': 'The Color Purple', 'director': 'Steven Spielberg', 'release_year': 1985}
]

@blp.route('/')
class Movies(MethodView):

    @blp.response(200, MovieSchema(many=True))
    def get(self):
        return movies

    @blp.arguments(MovieSchema)
    @blp.response(201, MovieSchema)
    def post(self, new_data):
        # Create a new movie entry
        new_id = max(movie['id'] for movie in movies) + 1
        new_data['id'] = new_id
        movies.append(new_data)
        return new_data

    @blp.arguments(MovieSchema)
    @blp.response(200, MovieSchema)
    @blp.route('/<int:movie_id>', methods=['PUT'])
    def put(self, update_data, movie_id):
        # Update an existing movie entry
        movie = next((movie for movie in movies if movie['id'] == movie_id), None)
        if not movie:
            abort(404, message="Movie not found")
        movie.update(update_data)
        return movie

    @blp.route('/<int:movie_id>', methods=['DELETE'])
    @blp.response(204)
    def delete(self, movie_id):
        # Delete a movie entry
        movie = next((movie for movie in movies if movie['id'] == movie_id), None)
        if not movie:
            abort(404, message="Movie not found")
        movies.remove(movie)
        return '', 204