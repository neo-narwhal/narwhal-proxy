import os

from flask import Flask
from flask_compress import Compress
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from app.config import config_by_name

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
compress = Compress()


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config_by_name[config_name])

    # Set up extensions
    db.init_app(app)
    compress.init_app(app)
    jwt = JWTManager(app)
    CORS(app, resources={"*": {"origins": "*"}})

    @jwt.user_claims_loader
    def add_claims_to_access_token(identity):
        return {
            'user_id': str(identity)
        }

    # Create app blueprints
    from .containers import blueprint as container_api
    app.register_blueprint(container_api)

    return app
