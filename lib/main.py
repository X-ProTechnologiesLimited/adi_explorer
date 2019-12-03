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
from . import movie_config

main = Blueprint('main', __name__, static_url_path='', static_folder='../created_adi/', template_folder='../templates')


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/create_package')
def create_package():
    return render_template('create_package.html')



@main.route('/create_package', methods=['POST'])
def create_adi():
    ts = time.time()
    asset_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
    asset_type = request.form.get('asset_type')
    LicenseWindow = int(request.form.get('LicenseWindow'))
    licenseEndTime = offerdate.offer_date(LicenseWindow,0)
    offer_window = int(request.form.get('offer_window'))

    if asset_type == 'EST':
        sitemap = 'EST_Sample.xml'
    elif asset_type == 'PREMIUM VOD':
        sitemap = 'PREMVOD_Sample.xml'
    else:
        return errorchecker.not_supported_asset_type(asset_type)

    values = []
    multiformat_id = request.form.get('multiformat_id')
    subtitle_lang = request.form.get('subtitle_lang')

    try:
        new_package = ADI_META(assetId=asset_timestamp + '01', original_timestamp=asset_timestamp, adi_type=asset_type, title=request.form.get('title'), provider_version=request.form.get('provider_version'),
                                    provider_id=request.form.get('provider_id'), offerStartTime=offerdate.offer_date(0,0), offerEndTime=offerdate.offer_date(offer_window,0),
                                    licenseEndTime=licenseEndTime, par_rating=request.form.get('par_rating'), subtitle_flag=request.form.get('subtitle_flag'),
                                    audio_type=request.form.get('audio_type'), frame_rate=request.form.get('frame_rate'), btc_rating=request.form.get('ca_btc'))

        db.session.add(new_package)
        db.session.commit()
    except:
        return errorchecker.internal_server_error()

    if multiformat_id != "":
        asset_mf_id = multiformat_id
        package = ADI_META.query.filter_by(assetId=asset_timestamp + '01').update(dict(multiformat_id=multiformat_id))
    else:
        asset_mf_id = 'BSKYPR' + asset_timestamp
        package = ADI_META.query.filter_by(assetId=asset_timestamp + '01').update(dict(multiformat_id='BSKYPR' + asset_timestamp))

    if subtitle_lang != "":
        subtitle_lang = subtitle_lang
        package = ADI_META.query.filter_by(assetId=asset_timestamp + '01').update(dict(subtitle_lang=subtitle_lang))
    else:
        subtitle_lang = ""


    if 'hdr' in request.form.get('provider_id'):
        asset_uhd_flag = 'HDR-HLG10'
        movie_url = movie_config.hdr_movie_file
        movie_checksum = movie_config.hdr_movie_checksum
        package = ADI_META.query.filter_by(assetId=asset_timestamp + '01').update(dict(uhd_flag=asset_uhd_flag))

    elif '4k' in request.form.get('provider_id'):
        asset_uhd_flag = 'SDR'
        movie_url = movie_config.sdr_movie_file
        movie_checksum = movie_config.sdr_movie_checksum
        package = ADI_META.query.filter_by(assetId=asset_timestamp + '01').update(dict(uhd_flag=asset_uhd_flag))
    elif 'est' in request.form.get('provider_id'):
        asset_uhd_flag = 'false'
        movie_url = movie_config.est_movie_file
        movie_checksum = movie_config.est_movie_checksum
    else:
        asset_uhd_flag = 'false'
        movie_url = movie_config.hd_movie_file
        movie_checksum = movie_config.hd_movie_checksum

    package = ADI_META.query.filter_by(assetId=asset_timestamp + '01').update(dict(movie_url=movie_url))
    package = ADI_META.query.filter_by(assetId=asset_timestamp + '01').update(dict(movie_checksum=movie_checksum))

    db.session.commit()

    values.append({
        'title': request.form.get('title'),
        'providerid': request.form.get('provider_id'),
        'assetid': asset_timestamp,
        'provider_version': request.form.get('provider_version'),
        'licensetime': licenseEndTime,
        'offerStartDateTime': offerdate.offer_date(0,0),
        'offerEndDateTime': offerdate.offer_date(offer_window,0),
        'multiformatid': asset_mf_id,
        'uhd_flag': asset_uhd_flag,
        'subtitle_flag': request.form.get('subtitle_flag'),
        'par_rating': request.form.get('par_rating'),
        'audio_type': request.form.get('audio_type'),
        'frame_rate': request.form.get('frame_rate'),
        'btc_rating': request.form.get('ca_btc'),
        'movie_url': movie_url,
        'movie_checksum': movie_checksum,
        'subtitle_lang': subtitle_lang
    })

    template = render_template(sitemap, values=values)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml; charset=utf-8'
    return response





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
            'multiformat_id': package.multiformat_id,
            'uhd_flag': package.uhd_flag
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
            'multiformat_id': package.multiformat_id,
            'uhd_flag': package.uhd_flag
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
    try:
        package = ADI_META.query.filter_by(assetId=assetId).first()
        if package.adi_type == 'EST':
            sitemap = 'EST_Sample.xml'
        elif package.adi_type == 'PREMIUM VOD':
            sitemap = 'PREMVOD_Sample.xml'
        else:
            return errorchecker.not_supported_asset_type(package.adi_type)

        values = []
        if package.uhd_flag == None:
            uhd_flag = 'false'
        else:
            uhd_flag = package.uhd_flag

        if package.subtitle_lang == None:
            subtitle_lang = ""
        else:
            subtitle_lang = package.subtitle_lang
        values.append({
            'title': package.title,
            'providerid': package.provider_id,
            'assetid': package.original_timestamp,
            'provider_version': package.provider_version,
            'licensetime': package.licenseEndTime,
            'offerStartDateTime': package.offerStartTime,
            'offerEndDateTime': package.offerEndTime,
            'multiformatid': package.multiformat_id,
            'uhd_flag': uhd_flag,
            'subtitle_flag': package.subtitle_flag,
            'par_rating': package.par_rating,
            'audio_type': package.audio_type,
            'frame_rate': package.frame_rate,
            'btc_rating': package.btc_rating,
            'movie_url': package.movie_url,
            'movie_checksum': package.movie_checksum,
            'subtitle_lang': subtitle_lang
        })

        template = render_template(sitemap, values=values)
        response = make_response(template)
        response.headers['Content-Type'] = 'application/xml'

        return response

    except:
        return errorchecker.asset_not_found_id(assetId)




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
    adi_metadata['packages']['Subtitle_Language'] = package.subtitle_lang

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
        package = ADI_META.query.filter_by(assetId=assetId).update(dict(movie_url=movie_url))
        package = ADI_META.query.filter_by(assetId=assetId).update(dict(movie_checksum=movie_checksum))
        db.session.commit()
        package_updated = ADI_META.query.filter_by(assetId=assetId).first()
        provider_version = int(package_updated.provider_version)
        updated_provider_version = (provider_version + 1)
        package = ADI_META.query.filter_by(assetId=assetId).update(dict(provider_version=str(updated_provider_version)))
        db.session.commit()
        return response.asset_update_success(assetId, 'movie')
    except:
        return errorchecker.asset_not_found_id(assetId)




@main.route('/quit')
def quit():
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return 'Appliation shutting down...'