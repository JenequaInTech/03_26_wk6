def configure_routes(app):
    
    movies = {
        '1': {'title': 'Love and Basketball', 'director': 'Gina Prince-Bythewood', 'release_date': '2000'},
        '2': {'title': "What's Love Got to Do with It", 'director': 'Brian Gibson', 'release_date': '1993'},
        '3': {'title': 'The Color Purple', 'director': 'Steven Spielberg', 'release_date': '1985'}
    }

    @app.route('/movies', methods=['GET'])
    def get_movies():
        return {'movies': list(movies.values())}

    @app.route('/movies/<id>', methods=['GET'])
    def get_movie(id):
        movie = movies.get(id, {})
        if movie:
            return movie
        else:
            return {"error": "Movie not found"}, 404

    @app.route('/movies', methods=['POST'])
    def add_movie():
        from flask import request
        movie_data = request.get_json()
        new_id = str(int(max(movies.keys(), key=int)) + 1)
        movies[new_id] = movie_data
        return movies[new_id], 201

    @app.route('/movies/<id>', methods=['PUT'])
    def update_movie(id):
        from flask import request
        movie_data = request.get_json()
        if id in movies:
            movies[id].update(movie_data)
            return movies[id]
        else:
            return {"error": "Movie not found"}, 404

    @app.route('/movies/<id>', methods=['DELETE'])
    def delete_movie(id):
        if id in movies:
            del movies[id]
            return {"message": "Movie deleted"}
        else:
            return {"error": "Movie not found"}, 404
        

        def configure_routes(app):
    # Movies data setup (existing code)
    # ...

    # Directors data setup
    directors = {
        '1': {'name': 'Spike Lee', 'nationality': 'American', 'years_active': '1977-present'},
        '2': {'name': 'Quentin Tarantino', 'nationality': 'American', 'years_active': '1987-present'}
    }

    # Directors Routes
    @app.route('/directors', methods=['GET'])
    def get_directors():
        return {'directors': list(directors.values())}

    @app.route('/directors', methods=['POST'])
    def add_director():
        from flask import request
        director_data = request.get_json()
        new_id = str(int(max(directors.keys(), key=int)) + 1)
        directors[new_id] = director_data
        return directors[new_id], 201

    @app.route('/directors/<id>', methods=['GET'])
    def get_director(id):
        director = directors.get(id, {})
        if director:
            return director
        else:
            return {"error": "Director not found"}, 404

    @app.route('/directors/<id>', methods=['PUT'])
    def update_director(id):
        from flask import request
        director_data = request.get_json()
        if id in directors:
            directors[id].update(director_data)
            return directors[id]
        else:
            return {"error": "Director not found"}, 404

    @app.route('/directors/<id>', methods=['DELETE'])
    def delete_director(id):
        if id in directors:
            del directors[id]
            return {"message": "Director deleted"}
        else:
            return {"error": "Director not found"}, 404