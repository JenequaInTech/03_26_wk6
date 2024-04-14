from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes import configure_routes
    configure_routes(app)

from flask import Flask
from flask_smorest import Api
from marshmallow import Schema, fields

def create_app():
    app = Flask(__name__)
    app.config['API_TITLE'] = 'My API'
    app.config['API_VERSION'] = 'v1'
    app.config['OPENAPI_VERSION'] = '3.0.2'
    app.config['OPENAPI_URL_PREFIX'] = '/api'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

    api = Api(app)
    from .movies import blp as movies_blp
    api.register_blueprint(movies_blp)

    return app