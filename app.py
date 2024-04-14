# app.py at the root of the project
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


# app/__init__.py
from flask import Flask
from .routes.movies import movies_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(movies_bp, url_prefix='/api')
    return app

