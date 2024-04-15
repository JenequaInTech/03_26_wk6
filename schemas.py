from marshmallow import Schema, fields, validate

class MovieSchema(Schema):
    id = fields.Int(dump_only=True)  # ID is not accepted as input, only for output
    title = fields.String(required=True, validate=validate.Length(min=1), error_messages={"required": "Title is required.", "too_short": "Title must not be empty."})
    director = fields.String(required=True, validate=validate.Length(min=1), error_messages={"required": "Director is required.", "too_short": "Director name must not be empty."})
    release_year = fields.Int(required=True, validate=validate.Range(min=1900, max=2100), error_messages={"required": "Release year is required.", "invalid_range": "Release year must be between 1900 and 2100."})

    from flask import request, jsonify
from .schemas import MovieSchema

@app.route('/movies', methods=['POST'])
def add_movie():
    schema = MovieSchema()
    try:
        # Validate and deserialize input
        movie_data = schema.load(request.get_json())
        # Logic to add the movie to the database
        new_movie = add_movie_to_db(movie_data)
        return jsonify(schema.dump(new_movie)), 201
    except ValidationError as err:
        return jsonify(err.messages), 400