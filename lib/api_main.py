# lib/api_main.py
"""
Created on May 27, 2020
@author: Krishnendu Banerjee
@summary: This file is responsible for creating basic APIS for the Flask applications.
"""
import os, hashlib, os.path
from flask import Blueprint, render_template, request, send_from_directory
from .nocache import nocache
from bson.json_util import dumps
from . import response, movie_config, load_default_data
path_to_script = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIRECTORY = movie_config.premium_upload_dir
VRP_PACKAGE_DIR = movie_config.premium_vrp_dir
TEMPLATE_DIR = os.path.abspath(movie_config.template_dir)


api_main = Blueprint('api_main', __name__)

######## Index and Defaults #########
@api_main.route('/')
def index(): # Load Index.html
    return render_template('index.html')

@api_main.route('/load_defaults')
def load_defaults(): # Load Default Media after we start with fresh database
    return load_default_data.load_default_media()



########### Media Management Routes ###############

@api_main.route("/files")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    json_data = dumps(files)
    return response.asset_retrieve(json_data)


@api_main.route("/files/<path:path>")
@nocache
def get_file(path):
    """Download a supporing file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

@api_main.route("/send_tar_files/<path:path>")
def send_tar_file(path):
    """Download a TAR File file."""
    return send_from_directory(VRP_PACKAGE_DIR, path, as_attachment=True)


########## API Shutdown Route ####################

@api_main.route('/quit')
def quit():
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return 'Appliation shutting down...'