# __init__.py

from flask import Flask
from . import movie_config
from flask_sqlalchemy import SQLAlchemy
import os
# Setting the flask jinja template render directories
TEMPLATE_DIR = os.path.abspath(movie_config.template_dir)
STATIC_DIR = os.path.abspath(movie_config.static_dir)

# Initializing the Database
db = SQLAlchemy()
# Creating the Flask Application for Asset Generator
def create_app():
    app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  # Specifying the database file
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app