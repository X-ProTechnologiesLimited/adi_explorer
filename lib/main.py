# main.py

from flask import Blueprint, render_template, request
from . import errorchecker
from .nocache import nocache
from . import create_asset
from . import search
from . import get_asset_details
from . import update_package
from .models import ADI_main

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

@main.route('/get_adi')
def get_adi():
    return render_template('retrieve_package.html')

@main.route('/get_adi', methods=['POST'])
def get_adi_post():
    try:
        assetId = request.form.get('AssetId')
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
    return get_asset_details.post_adi_endpoint(request.form.get('assetId'), request.form.get('environment'), request.form.get('source'))

@main.route('/quit')
def quit():
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return 'Appliation shutting down...'