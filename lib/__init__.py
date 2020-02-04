# __init__.py

from flask import Flask
from . import movie_config
from flask_sqlalchemy import SQLAlchemy
import os
TEMPLATE_DIR = os.path.abspath(movie_config.template_dir)
STATIC_DIR = os.path.abspath(movie_config.static_dir)

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS '] = False
    app.config['DEBUG'] = True

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app