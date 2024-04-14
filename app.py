from flask import Flask
from routes import configure_routes

def create_app():
    app = Flask(__name__)
    configure_routes(app)  # This will set up your routes from routes.py
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

  from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory 'database' for movies
movies = [
    {'id': 1, 'title': 'Love and Basketball', 'director': 'Gina Prince-Bythewood', 'release_year': 2000},
    {'id': 2, 'title': "What's Love Got to Do with It", 'director': 'Brian Gibson', 'release_year': 1993},
    {'id': 3, 'title': 'The Color Purple', 'director': 'Steven Spielberg', 'release_year': 1985}
]

@app.route('/movies', methods=['GET'])
def get_movies():
    return jsonify(movies)

@app.route('/movies', methods=['POST'])
def create_movie():
    if not request.json or not 'title' in request.json:
        abort(400)
    new_movie = {
        'id': movies[-1]['id'] + 1,
        'title': request.json['title'],
        'director': request.json.get('director', ""),
        'release_year': request.json.get('release_year', "")
    }
    movies.append(new_movie)
    return jsonify(new_movie), 201

@app.route('/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    movie = [movie for movie in movies if movie['id'] == movie_id]
    if len(movie) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'director' in request.json and type(request.json['director']) is not str:
        abort(400)
    if 'release_year' in request.json and type(request.json['release_year']) is not int:
        abort(400)

    movie[0]['title'] = request.json.get('title', movie[0]['title'])
    movie[0]['director'] = request.json.get('director', movie[0]['director'])
    movie[0]['release_year'] = request.json.get('release_year', movie[0]['release_year'])
    return jsonify(movie[0])

@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = [movie for movie in movies if movie['id'] == movie_id]
    if len(movie) == 0:
        abort(404)
    movies.remove(movie[0])
    return jsonify({'result': True})

if __name__ == '__main__':
    app.run(debug=True)  