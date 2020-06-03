# lib/api_util.py
"""
Created on May 27, 2020

@author: Krishnendu Banerjee
@summary: This file is responsible for creating the Admin APIs, OMDB APIs and HELP APIs

"""

import os, os.path
from flask import Blueprint, request, render_template, send_from_directory
from . import copy_to_tank, errorchecker, movie_config, api_view, delete, \
    api_media_library, db, response, get_asset_details, update_package, get_omdb_data
from .models import MEDIA_LIBRARY, ADI_main
VRP_PACKAGE_DIR = movie_config.premium_vrp_dir
UPLOAD_DIRECTORY = movie_config.premium_upload_dir

api_util = Blueprint('api_util', __name__)

# Admin APIs #

@api_util.route("/add_default_media", methods=['GET', 'POST'])
def add_default_media():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that adds default media to the tool on startup with new database
    :access: public.
    :method: get and post
    :return: get: Render Jinja Template templates/load_default_library.html
    :return: post: module: copy_to_tank; function: scp_default_video_from_tank()
    """
    if request.method == 'POST':
        return copy_to_tank.scp_default_video_from_tank()
    return render_template('load_default_library.html')

@api_util.route("/delete_tar", methods=['POST'])
def delete_tar_file_post():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that deletes specified VRP TAR package from tool
    :access: public.
    :method: post
    :return: Remaining Tar Files in System on successful deletion
    """
    filename = request.form.get('filename')
    try:
        os.remove(os.path.join(VRP_PACKAGE_DIR, filename))
    except FileNotFoundError:
        return errorchecker.no_supporting_file(filename)
    return api_view.list_tar_files()


@api_util.route("/delete_file", methods=['POST'])
def delete_file_post():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that deletes specified supporting files from tool
    :access: public.
    :method: post
    :return: Remaining Files in System on successful deletion
    """
    filename = request.form.get('filename')
    try:
        os.remove(os.path.join(UPLOAD_DIRECTORY, filename))
        delete.delete_supp_file(filename)
    except FileNotFoundError:
        return errorchecker.no_supporting_file(filename)
    return api_media_library.list_files_checksum()

@api_util.route("/delete_image_group", methods=['POST'])
def delete_image_group():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that deletes specified group of Images from tool
    :access: public.
    :method: post
    :return: Remaining Files in System on successful deletion
    """
    title = request.form.get('image_prefix')
    text_files = [f for f in os.listdir(UPLOAD_DIRECTORY) if f.startswith(title)]
    for item in text_files:
        os.remove(os.path.join(UPLOAD_DIRECTORY, item))
        delete.delete_supp_file(item)

    return api_media_library.list_files_checksum()


@api_util.route("/delete_asset", methods=["GET", "POST"])
def delete_asset():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that deletes specified supporting files from tool
    :access: public.
    :method: get and post
    :return: get : Render Template templates/delete_asset.html
    :return: post Successful Deletion
    """
    assetId = request.form.get('assetId')
    image_group_name = db.session.query(MEDIA_LIBRARY.image_group).distinct().filter(
        MEDIA_LIBRARY.image_group != 'None')
    if request.method == "POST":
        try:
            package = ADI_main.query.filter_by(assetId=assetId).first()
            if package.adi_type == 'est_episode':
                delete.delete_asset_est_episode(assetId)
            elif package.adi_type == 'est_season' or package.adi_type == 'est_show':
                delete.delete_asset_est_group(assetId)
            else:
                delete.delete_asset_standard(assetId)

            return response.asset_delete_success(assetId)
        except:
            return errorchecker.asset_not_found_id(assetId)

    return render_template('delete_asset.html', image_group_name=image_group_name)


@api_util.route("/view_default_config")
def view_default_config():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function to view default configurations in tool
    :access: public.
    :method: post
    :return: default media path configurations in tool
    """
    return get_asset_details.get_default_config()

@api_util.route("/update_default_config", methods=["GET", "POST"])
def update_default_config():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that updates default configurations in tool
    :access: public.
    :method: get and post
    :return: get : render templates/update_default_paths.html
    :return: post : module: update_package; function: update_default_fields()
    """
    if request.method == "POST":
        return update_package.update_default_fields()
    return render_template('update_default_paths.html')

# OMDB APIs #

@api_util.route("/consult_omdb")
def consult_omdb():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that renders consult_omdb.html
    :access: public.
    :method: get
    :return: get: render templates/consult_omdb.html
    """
    return render_template('consult_omdb.html')

@api_util.route("/consult_omdb", methods=['POST'])
def consult_omdb_post():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that returns Real Data from OMDB API searching with title
    :access: public.
    :method: get
    :form_input: title
    :return: Real Data from OMDB API searching with title
    """
    title = request.form.get('title')
    return get_omdb_data.get_omdb_data(title)

@api_util.route("/create_omdb_image", methods=['POST'])
def omdb_image_create():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that returns Real images based on approved sizes from IMDB
    :access: public.
    :method: post
    :form_input: title
    :return: Creates all the required images based on approved sizes from IMDB
    """
    title = request.form.get('title')
    consult_omdb_post()
    return get_omdb_data.omdb_image_create(title)


# HELP and GUIDE APIs #

@api_util.route("/help/<guide_type>")
def help(guide_type):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that returns specific guides from the chosen option
    :access: public.
    :method: post
    :param guide_type: genre/parental_rating/audio_type/provider_id/user_guide
    :return: Return the respective guide based on chosen user-option guide_type
    """
    if guide_type == 'genre':
        return render_template('sky_genre.html')
    elif guide_type == 'parental_rating':
        return render_template('sky_rating.html')
    elif guide_type == 'audio_type':
        return render_template('sky_audio_type.html')
    elif guide_type =='provider_id':
        return render_template('sky_provider_guide.html')
    elif guide_type =='user_guide':
        return send_from_directory(directory=UPLOAD_DIRECTORY,
                                   filename='Asset_Generator_User_Guide.pdf',
                                   mimetype='application/pdf')