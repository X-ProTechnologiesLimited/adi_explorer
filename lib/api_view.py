# lib/api_view.py
"""
Created on May 27, 2020

@author: Krishnendu Banerjee
@summary: This file is responsible for creating the View and Download Asset APIs:

"""
import os
from flask import Blueprint, render_template, request, send_from_directory
from .nocache import nocache
from .models import ADI_main
from . import errorchecker, search, get_asset_details, create_tar, movie_config, response, api_ingest
from bson.json_util import dumps
VRP_PACKAGE_DIR = movie_config.premium_vrp_dir

api_view = Blueprint('api_view', __name__)

@api_view.route('/search', methods=['GET', 'POST'])
def search_adi():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that calls to API to search assets by title
    :access: public
    :method: post
    :return: post: module: search; function: search_by_title
    """
    if request.method == 'POST':
        return search.search_by_title()
    return render_template('search.html')


@api_view.route('/expand_show/<title>')
def expand_show(title):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that calls the API to download Asset
    :access: public
    :method: post
    :param assetId: Asset ID of the show to expand
    :return: post: module: expand show details; function: expand_show(title)
    """
    try:
        return search.expand_est_show(title)
    except:
        return errorchecker.no_assets_in_db

@api_view.route('/search_all')
@nocache
def search_adi_all():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that calls to API to search all assets on the database
    :access: public
    :method: post
    :return: post: module: search; function: search_all_packages
    """
    return search.search_all_packages()

@api_view.route('/adi', methods=['POST'])
def get_form_adi():
    if request.form.get('AssetId') == None:
        return errorchecker.input_missing('AssetId_Radio')
    else:
        if 'form_view' in request.form:
            return get_adi()
        elif 'form_download' in request.form:
            return download_adi()
        elif 'form_est_offers' in request.form:
            return get_est_offers()
        elif 'form_metadata' in request.form:
            return get_asset_metadata()
        elif 'form_download_bs' in request.form:
            return download_box_set()
        elif 'form_ingest' in request.form:
            return render_template('post_adi.html', asset_id=request.form.get('AssetId'))
        elif 'form_clone' in request.form:
            return render_template('clone_adi.html', asset_id=request.form.get('AssetId'))
        elif 'form_ingest_history' in request.form:
            return api_ingest.get_ingest_history()
        elif 'form_update_meta' in request.form:
            return render_template('update_single_title.html', asset_id=request.form.get('AssetId'))
        elif 'form_update_mov' in request.form:
            return render_template('update_video.html', asset_id=request.form.get('AssetId'),
                                   movie_type='movie')
        elif 'form_update_prev' in request.form:
            return render_template('update_video.html', asset_id=request.form.get('AssetId'),
                                   movie_type='trailer')
        else:
            return 'Not Valid'


@api_view.route('/get_adi/<assetId>')
def get_back_adi(assetId):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that calls the API to download Asset
    :access: public
    :method: post
    :param assetId: Asset ID of the asset to download
    :return: post: module: get_asset_details; function: download_title(assetId)
    """
    try:
        package = ADI_main.query.filter_by(assetId=assetId).first()
        if package.adi_type == 'est_episode':
            return get_asset_details.download_est_episode(assetId)
        elif package.adi_type == 'est_season':
            return get_asset_details.download_est_season(assetId)
        elif package.adi_type == 'est_show':
            return get_asset_details.download_est_show(assetId)
        elif package.adi_type == 'EST SINGLE TITLE':
            return get_asset_details.download_est_single_title(assetId)
        else:
            return get_asset_details.download_title(assetId)
    except:
        return errorchecker.asset_not_found_id(assetId)


@api_view.route('/get_adi', methods=['GET', 'POST'])
def get_adi():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that calls the API to download Asset
    :access: public.
    :method: get and post
    :form_input: assetId
    :return: get: Return Jinja template for templates/asset_info.html, html_title='View ADI', html_action='get_adi'
    :return: post: module: self(api_view); function: get_back_adi()
    """
    assetId = request.form.get('AssetId')
    if request.method == 'POST':
        return get_back_adi(assetId)
    return render_template('asset_info.html', title='View ADI', action='/get_adi')


@api_view.route('/get_asset_metadata', methods=['GET', 'POST'])
@nocache
def get_asset_metadata():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that calls the API to download asset Metadada
    :access: public.
    :form_input: assetId
    :method: get and post
    :return: get: Return Jinja template for templates/asset_info.html html_title='Get Asset Metadata', html_action='get_asset_metadata'
    :return: post: module: get_asset_details; function: get_asset_data(assetId)
    """
    assetId = request.form.get('AssetId')
    if request.method == 'POST':
        return get_asset_details.get_asset_data(assetId)
    return render_template('asset_info.html', title='Get Asset Metadata', action='/get_asset_metadata')


@api_view.route("/get_est_offers", methods=['GET', 'POST'])
def get_est_offers():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that calls the API to return Offers Associated with the Asset
    :access: public.
    :form_input: assetId for EST Single Title and Shows
    :method: get and post
    :return: get: Return Jinja template for templates/asset_info.html html_title='Get EST Offers', html_action='get_est_offers'
    :return: post: module: get_asset_details; function: get_est_offers(assetId)
    """
    assetId = request.form.get('AssetId')
    if request.method == 'POST':
        return get_asset_details.get_est_offers(assetId)
    return render_template('asset_info.html', title='Get EST Offers', action='/get_est_offers')

@api_view.route("/download_box_set", methods=["GET", "POST"])
def download_box_set():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that calls the API to Download the Box-Set ADIs into a ZIP file
    :access: public.
    :form_input: assetId for EST Shows only
    :method: get and post
    :return: get: Return Jinja template for templates/asset_info.html html_title='Download Show', html_action='download_box_set'
    :return: post: module: create_tar; function: create_est_show_zip()
    """
    assetId = request.form.get('AssetId')
    if request.method == "POST":
        return create_tar.create_est_show_zip(assetId)
    return render_template('asset_info.html', title='Download Show', action='/download_box_set')


@api_view.route("/tar_files")
def list_tar_files():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that calls the API to list the VRP Tar files on the server
    :access: public
    method: get
    :return: a list of VRP TAR files in the tool directory (VRP_PACKAGE_DIR = movie_config.premium_vrp_dir)
    """
    files = []
    tar_files = [f for f in os.listdir(VRP_PACKAGE_DIR) if f.endswith('tar')]
    for filename in tar_files:
        path = os.path.join(VRP_PACKAGE_DIR, filename)
        if os.path.isfile(path):
            files.append(filename)
    json_data = dumps(files)
    return response.asset_retrieve(json_data)

@api_view.route("/download_tar_files", methods=['GET', 'POST'])
def get_tar_file():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that calls the API to Download Specific Tar Files from the Server
    :access: public
    :form_input: filename: The filename of the VRP TAR file to be downloaded
    :method: get, post
    :return: get: Return Jinja template for templates/get_tar.html
    :return: post: download from local VRP directory (VRP_PACKAGE_DIR = movie_config.premium_vrp_dir)
    """
    filename = request.form.get('filename')
    if request.method == 'POST':
        try:
            return send_from_directory(VRP_PACKAGE_DIR, filename, as_attachment=True)
        except:
            return errorchecker.no_supporting_file(filename)

    return render_template('get_tar.html')


@api_view.route("/download_adi")
def download_adi():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that calls the API to Download Specific Tar Files from the Server
    :access: public
    :form_input: filename: The filename of the VRP TAR file to be downloaded
    :method: get, post
    :return: get: Return Jinja template for templates/get_tar.html
    :return: post: download from local VRP directory (VRP_PACKAGE_DIR = movie_config.premium_vrp_dir)
    """
    assetId = request.form.get('AssetId')
    try:
        create_tar.get_adi_xml(assetId, 'adi.xml')
        return send_from_directory(movie_config.adi_xml_dir, 'adi.xml', as_attachment=True)
    except:
        return errorchecker.asset_not_found_id(assetId)