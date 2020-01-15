# main.py

from flask import Blueprint, render_template, request, jsonify, abort, send_from_directory, flash, redirect, url_for
import requests
import os
from . import db
from . import errorchecker
from .nocache import nocache
from . import create_asset
from . import search
from . import get_asset_details
from . import update_package
from .models import ADI_main, ADI_INGEST_HISTORY
from . import response
import datetime
import time
from bson.json_util import dumps
from .metadata_params import metadata_default_params
params = metadata_default_params()
path_to_script = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIRECTORY = "../created_adi"

main = Blueprint('main', __name__, static_url_path='', static_folder='../created_adi/', template_folder='../templates')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/create_single_title')
def create_single_title():
    return render_template('create_single_title.html')

@main.route('/create_single_title', methods=['POST'])
def create_single_title_post():
    return create_asset.create_single_title()

@main.route('/create_series_episode')
def create_series_episode():
    return errorchecker.not_implemented_yet()

@main.route('/create_est_show')
def create_est_show():
    return render_template('create_box_set.html')

@main.route('/create_est_show', methods=['POST'])
def create_est_show_post():
    return create_asset.create_est_show_adi()

@main.route('/search')
def search_adi():
    return render_template('search.html')

@main.route('/search', methods=['POST'])
@nocache
def search_adi_post():
    return search.search_by_title()

@main.route('/search_est')
def search_est():
    return render_template('search_est.html')

@main.route('/search_est', methods=['POST'])
@nocache
def search_est_post():
    return search.search_est_assets()

@main.route('/search_all')
@nocache
def search_adi_all():
    return search.search_all_packages()


@main.route('/get_adi/<assetId>')
def get_back_adi(assetId):
    try:
        package = ADI_main.query.filter_by(assetId=assetId).first()
        if package.adi_type == 'est_episode':
            return get_asset_details.download_est_episode(assetId)
        elif package.adi_type == 'est_season':
            return get_asset_details.download_est_season(assetId)
        elif package.adi_type == 'est_show':
            return get_asset_details.download_est_show(assetId)
        else:
            return get_asset_details.download_title(assetId)
    except:
        return errorchecker.asset_not_found_id('AssetId')

@main.route('/get_adi')
def get_adi():
    return render_template('retrieve_package.html')

@main.route('/get_adi', methods=['POST'])
def get_adi_post():
    assetId = request.form.get('AssetId')
    return get_back_adi(assetId)

@main.route('/get_asset_metadata')
def get_asset_metadata():
    return render_template('retrieve_metadata.html')

@main.route('/get_asset_metadata', methods=['POST'])
@nocache
def get_asset_metadata_post():
    assetId = request.form.get('AssetId')
    return get_asset_details.get_asset_data(assetId)

@main.route('/get_asset_video')
def get_asset_video():
    return render_template('retrieve_video.html')

@main.route('/get_asset_video', methods=['POST'])
@nocache
def get_asset_video_post():
    assetId = request.form.get('AssetId')
    return get_asset_details.get_asset_video(assetId)

@main.route('/update_single_title')
def update_single_title():
    return render_template('update_single_title.html')

@main.route('/update_single_title', methods=['POST'])
def update_single_title_post():
    return update_package.update_single_title()

@main.route('/update_video')
def update_video():
    return render_template('update_video.html')

@main.route('/update_video', methods=['POST'])
def update_video_post():
    return update_package.update_asset_video()

@main.route('/update_show_season')
def update_show_season():
    return errorchecker.not_implemented_yet()

@main.route('/post_adi')
def post_adi():
    return render_template('post_adi.html')

@main.route('/post_adi', methods=['POST'])
@nocache
def post_adi_post():
    my_filename = os.path.join(path_to_script, "adi.xml")
    ts = time.time()
    conversationId = datetime.datetime.fromtimestamp(ts).strftime('%d%H%M%S')
    environment = request.form.get('environment')
    params.environment_entry(environment)
    assetId = request.form.get('assetId')
    source = request.form.get('source')
    get_adi_url = 'http://localhost:5000/get_adi/'+assetId
    response_adi = requests.get(url=get_adi_url)
    with open(my_filename, 'w') as f:
        f.write(response_adi.text)
    endpoint_url = params.environment_url + 'source=' + source + '&conversationId=' + conversationId
    headers = {'Content-type': 'text/xml; charset=UTF-8'}
    data = open(my_filename, 'rb').read()
    post_response = {}
    try:
        response_post_adi = requests.post(url=endpoint_url, data=data, headers=headers)
        post_response['Status'] = '200'
        post_response['Message'] = 'AssetID: '+ assetId + ' ingested successfully'
        post_response['Endpoint'] = endpoint_url
        post_response['ConversationId'] = conversationId
        post_response['Endpoint_Response'] = response_post_adi.text
        package = ADI_main.query.filter_by(assetId=assetId).first()
        ingest_response = ADI_INGEST_HISTORY(assetId=assetId, provider_version=package.provider_version,
                                             environment=environment, conversationId=conversationId)
        db.session.add(ingest_response)
        db.session.commit()
    except:
        post_response['Status'] = '404'
        post_response['Message'] = 'Error connecting to Endpoint: '+ endpoint_url
        post_response['ConversationId'] = conversationId

    json_data = dumps(post_response)
    return response.asset_retrieve(json_data)


@main.route("/files")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return jsonify(files)


@main.route("/files/<path:path>")
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


@main.route("/post_files_post", methods=['GET', 'POST'])
def post_files_post():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            file.save(os.path.join(UPLOAD_DIRECTORY, file.filename))
            return 'success'
    return render_template('upload_files.html')


@main.route("/get_ingest_history")
def get_ingest_history():
    return render_template('ingest_history.html')

@main.route("/get_ingest_history", methods=['POST'])
def get_ingest_history_post():
    assetId = request.form.get('assetId')
    return search.search_ingest_history(assetId)


@main.route('/quit')
def quit():
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return 'Appliation shutting down...'