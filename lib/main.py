# main.py

from flask import Blueprint, render_template, request, jsonify, make_response
import datetime
import time
from . import db
from .models import ADI_META
from . import errorchecker
from . import offerdate
import urllib.parse
from .nocache import nocache
from bson.json_util import dumps
from . import response
from . import package_logic

main = Blueprint('main', __name__, static_url_path='', static_folder='../created_adi/', template_folder='../templates')


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/create_single_title')
def create_single_title():
    return render_template('create_single_title.html')

@main.route('/create_single_title', methods=['POST'])
def create_single_title_post():
    ts = time.time()
    asset_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
    LicenseWindow = int(request.form.get('LicenseWindow'))
    licenseEndTime = offerdate.offer_date(LicenseWindow,0)
    offer_window = int(request.form.get('offer_window'))
    offerStartTime = offerdate.offer_date(0, 0)
    offerEndTime = offerdate.offer_date(offer_window, 0)
    asset_type = request.form.get('asset_type')
    multiformat_id = request.form.get('multiformat_id')
    subtitle_flag = request.form.get('subtitle_flag')
    provider_id = request.form.get('provider_id')
    title = request.form.get('title')
    provider_version = request.form.get('provider_version')
    par_rating = request.form.get('par_rating')
    audio_type = request.form.get('audio_type')
    frame_rate = request.form.get('frame_rate')
    btc_rating = request.form.get('ca_btc')
    asset_mf_id = package_logic.multiformat_entry(multiformat_id, asset_timestamp)
    movie_url = package_logic.movie_file_entry(provider_id)
    movie_checksum = package_logic.movie_checksum_entry(provider_id)
    video_type = package_logic.video_type_entry(provider_id)
    offer_type = package_logic.offer_type_entry(asset_type)

    sitemap = package_logic.sitemap_entry(asset_type, subtitle_flag)
    if sitemap == False:
        return errorchecker.not_supported_asset_type(asset_type)

    try:
        new_package = ADI_META(assetId=asset_timestamp + '01', original_timestamp=asset_timestamp,
                               adi_type=asset_type, title=title, provider_version=provider_version,
                               provider_id=provider_id, offerStartTime=offerStartTime,
                               offerEndTime=offerEndTime,licenseEndTime=licenseEndTime,
                               par_rating=par_rating, subtitle_flag=subtitle_flag, audio_type=audio_type,
                               frame_rate=frame_rate, btc_rating=btc_rating, multiformat_id=asset_mf_id,
                               movie_url=movie_url, movie_checksum=movie_checksum, offer_type=offer_type,
                               video_type=video_type)

        db.session.add(new_package)
        db.session.commit()
    except:
        return errorchecker.internal_server_error()

    return package_logic.download_adi_package(asset_timestamp + '01')


@main.route('/create_series_episode')
def create_series_episode():
    return errorchecker.not_implemented_yet()

@main.route('/create_est_box_set')
def create_est_box_set():
    return errorchecker.not_implemented_yet()


@main.route('/search')
def search_adi():
    return render_template('search.html')

@main.route('/search', methods=['POST'])
@nocache
def search_adi_post():
    title = request.form.get('Title')
    title_uncoded = urllib.parse.unquote_plus(title)
    adi_data = {}
    adi_data['packages'] = []
    search = "{}%".format(title_uncoded)
    for package in ADI_META.query.filter(ADI_META.title.like(search)).all():
        adi_data['packages'].append({
            'title': package.title,
            'assetId': package.assetId,
            'package_type': package.adi_type,
            'providerVersionNum': package.provider_version,
            'providerId': package.provider_id,
            'offerEndDateTime': package.offerEndTime,
            'multiformat_id': package.multiformat_id
        })

    adi_data['total'] = ADI_META.query.filter(ADI_META.title.like(search)).count()

    if adi_data['total'] == 0:  # If no ADI found
        return errorchecker.not_matched_criteria()
    else:
        json_data = dumps(adi_data, sort_keys=True)

    return response.asset_retrieve(json_data)




@main.route('/search_all')
@nocache
def search_adi_all():
    adi_data = {}
    adi_data['packages'] = []
    for package in ADI_META.query.all():
        adi_data['packages'].append({
            'title': package.title,
            'assetId': package.assetId,
            'package_type': package.adi_type,
            'providerVersionNum': package.provider_version,
            'providerId': package.provider_id,
            'offerEndDateTime': package.offerEndTime,
            'multiformat_id': package.multiformat_id
        })

    adi_data['total'] = ADI_META.query.count()

    if adi_data['total'] == 0:  # If no countries found in the continent
        return errorchecker.no_assets_in_db()
    else:
        json_data = dumps(adi_data, sort_keys=True)

    return response.asset_retrieve(json_data)


@main.route('/get_adi')
def get_adi():
    return render_template('retrieve_package.html')

@main.route('/get_adi', methods=['POST'])
def get_adi_post():
    assetId = request.form.get('AssetId')
    return package_logic.download_adi_package(assetId)



@main.route('/get_asset_metadata')
def get_asset_metadata():
    return render_template('retrieve_metadata.html')

@main.route('/get_asset_metadata', methods=['POST'])
@nocache
def get_asset_metadata_post():
    assetId = request.form.get('AssetId')
    adi_metadata = {}
    adi_metadata['packages'] = {}
    package = ADI_META.query.filter_by(assetId=assetId).first()
    if not package:
        return errorchecker.asset_not_found_id(AssetId)

    adi_metadata['packages']['assetId'] = package.assetId
    adi_metadata['packages']['title'] = package.title
    adi_metadata['packages']['audio_type'] = package.audio_type
    adi_metadata['packages']['Parental Rating'] = package.par_rating
    adi_metadata['packages']['CA/BTC Rating'] = package.btc_rating
    adi_metadata['packages']['Subtitle'] = package.subtitle_flag

    json_data = dumps(adi_metadata)
    return response.asset_retrieve(json_data)




@main.route('/get_asset_video')
def get_asset_video():
    return render_template('retrieve_video.html')

@main.route('/get_asset_video', methods=['POST'])
@nocache
def get_asset_video_post():
    assetId = request.form.get('AssetId')
    adi_metadata = {}
    adi_metadata['packages'] = {}
    package = ADI_META.query.filter_by(assetId=assetId).first()
    if not package:
        return errorchecker.asset_not_found_id(AssetId)

    adi_metadata['packages']['assetId'] = package.assetId
    adi_metadata['packages']['title'] = package.title
    adi_metadata['packages']['Movie File'] = package.movie_url
    adi_metadata['packages']['Movie Checksum'] = package.movie_checksum

    json_data = dumps(adi_metadata)
    return response.asset_retrieve(json_data)




@main.route('/update_package')
def update_package():
    return render_template('update_package.html')


@main.route('/update_package', methods=['POST'])
def update_package_post():
    assetId = request.form.get('AssetId')
    update_field = request.form.get('asset_field')
    field_value = request.form.get('value')
    try:
        package = ADI_META.query.filter_by(assetId=assetId).first()
        if update_field == 'title':
            package = ADI_META.query.filter_by(assetId=assetId).update(dict(title=field_value))
        elif update_field == 'offerStartTime':
            package = ADI_META.query.filter_by(assetId=assetId).update(dict(offerStartTime=field_value))
        elif update_field == 'offerEndTime':
            package = ADI_META.query.filter_by(assetId=assetId).update(dict(offerEndTime=field_value))
        elif update_field == 'licenseEndTime':
            package = ADI_META.query.filter_by(assetId=assetId).update(dict(licenseEndTime=field_value))
        elif update_field == 'audio_type':
            package = ADI_META.query.filter_by(assetId=assetId).update(dict(audio_type=field_value))
        elif update_field == 'frame_rate':
            package = ADI_META.query.filter_by(assetId=assetId).update(dict(frame_rate=field_value))
        elif update_field == 'par_rating':
            package = ADI_META.query.filter_by(assetId=assetId).update(dict(par_rating=field_value))
        elif update_field == 'btc_rating':
            package = ADI_META.query.filter_by(assetId=assetId).update(dict(btc_rating=field_value))
        elif update_field == 'subtitle_flag':
            package = ADI_META.query.filter_by(assetId=assetId).update(dict(subtitle_flag=field_value))
        elif update_field == 'multiformat_id':
            package = ADI_META.query.filter_by(assetId=assetId).update(dict(multiformat_id=field_value))
        elif update_field == 'subtitle_lang':
            package = ADI_META.query.filter_by(assetId=assetId).update(dict(subtitle_lang=field_value))
        else:
            return errorchecker.undefined_update_field(update_field)

        db.session.commit()
        package_updated = ADI_META.query.filter_by(assetId=assetId).first()
        provider_version = int(package_updated.provider_version)
        updated_provider_version = (provider_version + 1)
        package = ADI_META.query.filter_by(assetId=assetId).update(dict(provider_version=str(updated_provider_version)))
        db.session.commit()
        return response.asset_update_success(assetId, update_field)
    except:
        return errorchecker.asset_not_found_id(assetId)





@main.route('/update_video')
def update_video():
    return render_template('update_video.html')


@main.route('/update_video', methods=['POST'])
def update_video_post():
    assetId = request.form.get('AssetId')
    movie_url = request.form.get('movie_url')
    movie_checksum = request.form.get('movie_checksum')
    try:
        package = ADI_META.query.filter_by(assetId=assetId).first()
        provider_version = int(package.provider_version)
        updated_provider_version = (provider_version + 1)
        package = ADI_META.query.filter_by(assetId=assetId).update(dict(movie_url=movie_url, movie_checksum=movie_checksum,
                                                                        provider_version=str(updated_provider_version)))
        db.session.commit()
        return response.asset_update_success(assetId, 'movie')
    except:
        return errorchecker.asset_not_found_id(assetId)




@main.route('/quit')
def quit():
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return 'Appliation shutting down...'