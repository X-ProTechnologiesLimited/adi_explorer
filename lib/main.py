# main.py
from flask import Blueprint, render_template, request, send_from_directory, flash, redirect, Response
from .nocache import nocache
from .models import ADI_main, MEDIA_LIBRARY, ADI_offer
from bson.json_util import dumps
from .metadata_params import metadata_default_params
from . import db
import os
import hashlib
import os.path
from . import errorchecker, create_asset, search, get_asset_details, update_package, response, create_tar, movie_config
from . import delete, load_default_data, copy_to_tank, get_omdb_data, create_omdb_image
params = metadata_default_params()
path_to_script = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIRECTORY = movie_config.premium_upload_dir
VRP_PACKAGE_DIR = movie_config.premium_vrp_dir
TEMPLATE_DIR = os.path.abspath(movie_config.template_dir)


main = Blueprint('main', __name__)

######## Index and Defaults #########
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/load_defaults')
def load_defaults():
    return load_default_data.load_default_media()

@main.route("/add_default_media", methods=['GET', 'POST'])
def add_default_media():
    if request.method == 'POST':
        return copy_to_tank.scp_default_video_from_tank()
    return render_template('load_default_library.html')

######## Create Asset Routes #########

@main.route('/create_single_title/<package>', methods=['GET', 'POST'])
def create_single_title(package):
    video_filename = 'ts'
    search = "%{}%".format(video_filename)
    library = MEDIA_LIBRARY.query.filter(MEDIA_LIBRARY.filename.like(search))
    image_group_name = db.session.query(MEDIA_LIBRARY.image_group).distinct().filter(MEDIA_LIBRARY.image_group != 'None')
    if request.method == 'POST':
        return create_asset.create_single_title()
    return render_template('create_single_title.html', library=library, image_group_name=image_group_name, package=package)


@main.route('/create_est/<package>', methods=['GET', 'POST'])
def create_est(package):
    video_filename = 'ts'
    search = "%{}%".format(video_filename)
    library = MEDIA_LIBRARY.query.filter(MEDIA_LIBRARY.filename.like(search))
    image_group_name = db.session.query(MEDIA_LIBRARY.image_group).distinct().filter(MEDIA_LIBRARY.image_group != 'None')
    if package == 'show':
        if request.method == 'POST':
            return create_asset.create_est_show_adi()
        return render_template('create_box_set.html', library=library, image_group_name=image_group_name)
    elif package == 'single_title':
        if request.method == 'POST':
            return create_asset.create_est_title_adi()
        return render_template('create_est_title.html', library=library, image_group_name=image_group_name)
    else:
        return errorchecker.not_supported_asset_type(package)


@main.route("/create_tar", methods=['GET', 'POST'])
def make_tarfile():
    filename = request.form.get('filename')
    if request.method == 'POST':
        return create_tar.make_tarfile(filename)
    return render_template('create_tar.html')

@main.route("/clone_adi", methods=['GET', 'POST'])
def clone_adi():
    if request.method == 'POST':
        return create_asset.clone_asset()
    return render_template('clone_adi.html')



########### Search Asset Routes ##############

@main.route('/search')
def search_adi():
    return render_template('search.html')

@main.route('/search', methods=['POST'])
@nocache
def search_adi_post():
    return search.search_by_title()

@main.route('/search_est', methods=['POST'])
@nocache
def search_est_post():
    return search.search_est_assets()

@main.route('/search_all')
@nocache
def search_adi_all():
    return search.search_all_packages()


########## Download ADI and View Metadata Routes #############

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


@main.route('/get_adi', methods=['GET', 'POST'])
def get_adi():
    assetId = request.form.get('AssetId')
    if request.method == 'POST':
        return get_back_adi(assetId)
    return render_template('asset_info.html', title='View ADI', action='/get_adi')


@main.route('/get_asset_metadata', methods=['GET', 'POST'])
@nocache
def get_asset_metadata():
    assetId = request.form.get('AssetId')
    if request.method == 'POST':
        return get_asset_details.get_asset_data(assetId)
    return render_template('asset_info.html', title='Get Asset Metadata', action='/get_asset_metadata')


@main.route("/get_est_offers", methods=['GET', 'POST'])
def get_est_offers():
    assetId = request.form.get('AssetId')
    if request.method == 'POST':
        return get_asset_details.get_est_offers(assetId)
    return render_template('asset_info.html', title='Get EST Offers', action='/get_est_offers')

@main.route("/download_box_set", methods=["GET", "POST"])
def download_box_set():
    assetId = request.form.get('AssetId')
    if request.method == "POST":
        return create_tar.create_est_show_zip(assetId)
    return render_template('asset_info.html', title='Download Show', action='/download_box_set')


######## Update Asset Routes #################

@main.route('/update_single_title', methods=['GET', 'POST'])
def update_single_title():
    if request.method == 'POST':
        return update_package.update_single_title()
    return render_template('update_single_title.html')


@main.route('/update_video/<movie_type>', methods=['GET', 'POST'])
def update_video(movie_type):
    if request.method == 'POST':
        return update_package.update_asset_video(movie_type)
    return render_template('update_video.html', movie_type=movie_type)


########### Ingest and Post ADI Routes ############

@main.route('/post_adi', methods=['GET', 'POST'])
@nocache
def post_adi():
    if request.method == 'POST':
        return get_asset_details.post_adi_endpoint()
    return render_template('post_adi.html')

@main.route("/get_ingest_history", methods=['GET', 'POST'])
def get_ingest_history():
    assetId = request.form.get('AssetId')
    if request.method == 'POST':
        return search.search_ingest_history(assetId)
    return render_template('asset_info.html', title='Get Ingest History', action='/get_ingest_history')



########### Media Management Routes ###############

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
    tar_files = [f for f in os.listdir(VRP_PACKAGE_DIR) if f.endswith('tar')]
    for filename in tar_files:
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

@main.route("/download_tar_files", methods=['GET', 'POST'])
def get_tar_file():
    """Download a file."""
    filename = request.form.get('filename')
    if request.method == 'POST':
        try:
            return send_from_directory(VRP_PACKAGE_DIR, filename, as_attachment=True)
        except:
            return errorchecker.no_supporting_file(filename)

    return render_template('get_tar.html')

def checksum_creator(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


@main.route("/post_files_post", methods=["GET", "POST"])
def post_files_post():
    if request.method == "POST":
        file = request.files['file']
        file.save(os.path.join(UPLOAD_DIRECTORY, file.filename))
        image_group = request.form.get('image_group')
        checksum = checksum_creator(os.path.join(UPLOAD_DIRECTORY, file.filename))
        create_tar.add_supporting_files_to_db(file.filename, checksum, image_group)
        return list_files_checksum()
    return render_template('upload_files.html')

@main.route("/upload_to_tank", methods=["GET", "POST"])
def upload_to_tank():
    if request.method == "POST":
        return copy_to_tank.scp_to_tank()
    return render_template('upload_to_tank.html')

@main.route("/upload_to_jump", methods=["GET", "POST"])
def upload_to_jump():
    if request.method == "POST":
        return copy_to_tank.scp_to_jump()
    return render_template('upload_to_jump.html')


@main.route("/download_from_tank", methods=["GET", "POST"])
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


############# Admin and Delete Routes ################

@main.route("/delete_tar", methods=['POST'])
def delete_tar_file_post():
    filename = request.form.get('filename')
    try:
        os.remove(os.path.join(VRP_PACKAGE_DIR, filename))
    except FileNotFoundError:
        return errorchecker.no_supporting_file(filename)
    return list_tar_files()


@main.route("/delete_file", methods=['POST'])
def delete_file_post():
    filename = request.form.get('filename')
    try:
        os.remove(os.path.join(UPLOAD_DIRECTORY, filename))
        delete.delete_supp_file(filename)
    except FileNotFoundError:
        return errorchecker.no_supporting_file(filename)
    return list_files()


@main.route("/delete_asset", methods=["GET", "POST"])
def delete_asset():
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


@main.route("/view_default_config")
def view_default_config():
    return get_asset_details.get_default_config()


@main.route("/update_default_config", methods=["GET", "POST"])
def update_default_config():
    if request.method == "POST":
        return update_package.update_default_fields()
    return render_template('update_default_paths.html')


########### CONSULT OMDB Routes ##############

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
    consult_omdb_post()
    return create_omdb_image.omdb_image_create(title)


############# HELP and GUIDE Routes ##############

@main.route("/help/<guide_type>")
def help(guide_type):
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


########## API Shutdown Route ####################

@main.route('/quit')
def quit():
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return 'Appliation shutting down...'