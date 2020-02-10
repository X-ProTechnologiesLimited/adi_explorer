# main.py

from flask import Blueprint, render_template, request, send_from_directory, flash, redirect
from .nocache import nocache
from .models import ADI_main, MEDIA_LIBRARY
from bson.json_util import dumps
from .metadata_params import metadata_default_params
import os
import hashlib
import os.path
from . import errorchecker, create_asset, search, get_asset_details, update_package, response, create_tar, movie_config
from . import delete, load_default_data, copy_to_tank, get_omdb_data, create_omdb_image
params = metadata_default_params()
path_to_script = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIRECTORY = movie_config.premium_upload_dir
VRP_PACKAGE_DIR = movie_config.premium_vrp_dir


main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/load_defaults')
def load_defaults():
    return load_default_data.load_default_media()

@main.route('/create_single_title_standard')
def create_single_title_standard():
    return render_template('create_single_title_standard.html')

@main.route('/create_single_title_standard', methods=['POST'])
def create_single_title_standard_post():
    return create_asset.create_single_title()

@main.route('/create_single_title_vrp')
def create_single_title_vrp():
    return render_template('create_single_title_vrp.html')

@main.route('/create_single_title_vrp', methods=['POST'])
def create_single_title_vrp_post():
    return create_asset.create_single_title()

@main.route('/create_est_show')
def create_est_show():
    return render_template('create_box_set.html')

@main.route('/create_est_show', methods=['POST'])
def create_est_show_post():
    return create_asset.create_est_show_adi()

@main.route('/create_est_single_title')
def create_est_single_title():
    return render_template('create_est_title.html')

@main.route('/create_est_single_title', methods=['POST'])
def create_est_single_title_post():
    return create_asset.create_est_title_adi()

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
        elif package.adi_type == 'EST SINGLE TITLE':
            return get_asset_details.download_est_single_title(assetId)
        else:
            return get_asset_details.download_title(assetId)
    except:
        return errorchecker.asset_not_found_id(assetId)

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
    return get_asset_details.post_adi_endpoint()

@main.route("/files")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    json_data = dumps(files)
    return response.asset_retrieve(json_data)

@main.route("/delete_image_group", methods=['POST'])
def delete_image_group():
    """Endpoint to list files on the server."""
    title = request.form.get('image_prefix')
    text_files = [f for f in os.listdir(UPLOAD_DIRECTORY) if f.startswith(title)]
    for item in text_files:
        os.remove(os.path.join(UPLOAD_DIRECTORY, item))
        delete.delete_supp_file(item)

    return list_files()


@main.route("/get_file_list_checksum")
def list_files_checksum():
    """Endpoint to list files on the server."""
    return search.search_all_files_checksum()

@main.route("/tar_files")
def list_tar_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(VRP_PACKAGE_DIR):
        path = os.path.join(VRP_PACKAGE_DIR, filename)
        if os.path.isfile(path):
            files.append(filename)
    json_data = dumps(files)
    return response.asset_retrieve(json_data)



@main.route("/files/<path:path>")
@nocache
def get_file(path):
    """Download a file."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)

@main.route("/send_tar_files/<path:path>")
def send_tar_file(path):
    """Download a file."""
    return send_from_directory(VRP_PACKAGE_DIR, path, as_attachment=True)


@main.route("/download_tar_files")
def get_tar_file():
    """Download a file."""
    return render_template('get_tar.html')


@main.route("/download_tar_files", methods=['POST'])
def get_tar_file_post():
    """Download a file."""
    filename = request.form.get('filename')
    try:
        return send_from_directory(VRP_PACKAGE_DIR, filename, as_attachment=True)
    except:
        return errorchecker.no_supporting_file(filename)

def checksum_creator(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


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
            checksum = checksum_creator(os.path.join(UPLOAD_DIRECTORY, file.filename))
            create_tar.add_supporting_files_to_db(file.filename, checksum)
            return list_files()
    return render_template('upload_files.html')


@main.route("/delete_tar")
def delete_tar_file():
    return render_template('delete_tar.html')

@main.route("/delete_tar", methods=['POST'])
def delete_tar_file_post():
    filename = request.form.get('filename')
    try:
        os.remove(os.path.join(VRP_PACKAGE_DIR, filename))
    except FileNotFoundError:
        return errorchecker.no_supporting_file(filename)
    return list_tar_files()

@main.route("/delete_file")
def delete_file():
    return render_template('delete_supp_file.html')

@main.route("/delete_file", methods=['POST'])
def delete_file_post():
    filename = request.form.get('filename')
    try:
        os.remove(os.path.join(UPLOAD_DIRECTORY, filename))
        delete.delete_supp_file(filename)
    except FileNotFoundError:
        return errorchecker.no_supporting_file(filename)
    return list_files()


@main.route("/delete_asset")
def delete_asset():
    return render_template('delete_asset.html')

@main.route("/delete_asset", methods=['POST'])
def delete_asset_post():
    assetId = request.form.get('assetId')
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

@main.route("/get_ingest_history")
def get_ingest_history():
    return render_template('ingest_history.html')

@main.route("/get_ingest_history", methods=['POST'])
def get_ingest_history_post():
    assetId = request.form.get('assetId')
    return search.search_ingest_history(assetId)

@main.route("/create_tar")
def make_tarfile():
    return render_template('create_tar.html')

@main.route("/create_tar", methods=['POST'])
def make_tarfile_post():
    return create_tar.make_tarfile()


@main.route("/upload_to_tank")
def upload_to_tank():
    return render_template('upload_to_tank.html')

@main.route("/upload_to_tank", methods=['POST'])
def upload_to_tank_post():
    return copy_to_tank.scp_to_tank()

@main.route("/consult_omdb")
def consult_omdb():
    return render_template('consult_omdb.html')

@main.route("/consult_omdb", methods=['POST'])
def consult_omdb_post():
    title = request.form.get('title')
    return get_omdb_data.get_omdb_data(title)

@main.route("/create_omdb_image", methods=['POST'])
def omdb_image_create():
    title = request.form.get('title')
    return create_omdb_image.omdb_image_create(title)

@main.route("/view_default_config")
def view_default_config():
    return get_asset_details.get_default_config()


@main.route("/update_default_config")
def update_default_config():
    return render_template('update_default_paths.html')

@main.route("/update_default_config", methods=['POST'])
def update_default_config_post():
    return update_package.update_default_fields()


@main.route('/quit')
def quit():
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return 'Appliation shutting down...'