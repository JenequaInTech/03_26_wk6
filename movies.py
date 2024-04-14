from flask.views import MethodView
from flask_smorest import Blueprint, abort
from .schemas import MovieSchema

blp = Blueprint('movies', 'movies', url_prefix='/movies', description='Operations on movies')

@blp.route('/')
class Movies(MethodView):

    @blp.response(200, MovieSchema(many=True))
    def get(self):
        # Assume movies is a dictionary of movies
        return list(movies.values())

    @blp.arguments(MovieSchema)
    @blp.response(201, MovieSchema)
    def post(self, new_data):
        # Logic to add a movie
        pass