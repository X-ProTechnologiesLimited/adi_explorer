# lib/__init__.py
"""
Created on Nov 29, 2019

@author: Krishnendu Banerjee
@summary: This file is responsible for creating the main flask application:

"""
import os
from flask import Flask
from . import movie_config
from flask_sqlalchemy import SQLAlchemy

# Setting the flask jinja template render directories
TEMPLATE_DIR = os.path.abspath(movie_config.template_dir)
STATIC_DIR = os.path.abspath(movie_config.static_dir)

# Initializing the Database
db = SQLAlchemy()

# Creating the Flask Application for Asset Generator
def create_app():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Creates Main Flask Application for ADI manager.
    :access: public.
    """
    app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

    # Setting the Flask application configuration
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  # Specifying the database file
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    db.init_app(app) # Initialise the application

    from .api_main import api_main as api_main_blueprint  # Import the API module
    app.register_blueprint(api_main_blueprint) # Register application

    from .api_create_package import api_create_package as api_create_package_blueprint  # Import the Create API Module
    app.register_blueprint(api_create_package_blueprint)  # Register Module

    from .api_view import api_view as api_view_blueprint  # Import the Search and Get Modules
    app.register_blueprint(api_view_blueprint)  # Register Modules

    from .api_update import api_update as api_update_blueprint  # Import the Asset Update Module
    app.register_blueprint(api_update_blueprint)  # Register Modules

    from .api_ingest import api_ingest as api_ingest_blueprint # Import the Asset Update Module
    app.register_blueprint(api_ingest_blueprint) # Register Modules

    from .api_media_library import api_media_library as api_media_library_blueprint  # Import the Media Library Module
    app.register_blueprint(api_media_library_blueprint)  # Register Modules

    from .api_util import api_util as api_util_blueprint  # Import the Admin, OMDB and HELP modules
    app.register_blueprint(api_util_blueprint)  # Register Modules

    return app # Creates and returns the flask application