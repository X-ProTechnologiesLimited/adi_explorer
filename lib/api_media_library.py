# lib/api_media_library.py
"""
Created on May 27, 2020

@author: Krishnendu Banerjee
@summary: This file is responsible for creating the Media Library APIs

"""
import os, hashlib, os.path
from flask import Blueprint, request, render_template
from . import search,create_tar, movie_config, copy_to_tank, errorchecker
UPLOAD_DIRECTORY = movie_config.premium_upload_dir

api_media_library = Blueprint('api_media_library', __name__)

def checksum_creator(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()

@api_media_library.route("/get_file_list_checksum")
def list_files_checksum():
    """Endpoint to list files on the server."""
    return search.search_all_files_checksum()


@api_media_library.route("/post_files_post", methods=["GET", "POST"])
def post_files_post():
    if request.method == "POST":
        file = request.files['file']
        file.save(os.path.join(UPLOAD_DIRECTORY, file.filename))
        image_group = request.form.get('image_group')
        checksum = checksum_creator(os.path.join(UPLOAD_DIRECTORY, file.filename))
        create_tar.add_supporting_files_to_db(file.filename, checksum, image_group)
        return list_files_checksum()
    return render_template('upload_files.html')

@api_media_library.route("/download_from_tank", methods=["GET", "POST"])
def download_from_tank():
    if request.method == "POST":
        filename = request.form.get('filename')
        tank_path = request.form.get('tank_path')
        image_group = request.form.get('image_group')
        copy_to_tank.scp_file_from_tank(tank_path, filename)
        files_to_copy = [f for f in os.listdir(UPLOAD_DIRECTORY) if f.startswith(filename[:-1])]
        for item in files_to_copy:
            try:
                checksum = checksum_creator(os.path.join(UPLOAD_DIRECTORY, item))
                create_tar.add_supporting_files_to_db(item, checksum, image_group)
            except FileNotFoundError:
                return errorchecker.upload_filenotfound_error(item)
        return list_files_checksum()
    return render_template('upload_to_tank.html')


@api_media_library.route("/upload_to_tank", methods=["GET", "POST"])
def upload_to_tank():
    if request.method == "POST":
        return copy_to_tank.scp_to_tank()
    return render_template('upload_to_tank.html')

@api_media_library.route("/upload_to_jump", methods=["GET", "POST"])
def upload_to_jump():
    if request.method == "POST":
        return copy_to_tank.scp_to_jump()
    return render_template('upload_to_jump.html')