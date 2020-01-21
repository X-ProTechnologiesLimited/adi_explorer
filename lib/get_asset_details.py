from flask import Blueprint, render_template, make_response, request
from .models import ADI_main, ADI_media, ADI_metadata, ADI_offer, ADI_EST_Show
from . import movie_config
from .sitemap_create import sitemap_mapper
from bson.json_util import dumps
from . import response
import datetime
import time
from .metadata_params import metadata_default_params
from . import errorchecker
import requests
import os
from . import db
from .models import ADI_main, ADI_INGEST_HISTORY
path_to_script = os.path.dirname(os.path.abspath(__file__))
params = metadata_default_params()
sitemap = sitemap_mapper()

main = Blueprint('main', __name__, static_url_path='', static_folder='../premium_files/', template_folder='../templates')

def download_title(assetId):
    try:
        package_main = ADI_main.query.filter_by(assetId=assetId).first()
        package_meta = ADI_metadata.query.filter_by(assetId=assetId).first()
        package_offer = ADI_offer.query.filter_by(assetId=assetId).first()
        package_media = ADI_media.query.filter_by(assetId=assetId).first()
        sitemap.sitemap_entry(package_main.adi_type, package_meta.subtitle_flag)
        asset_duration = 'PT'+package_meta.duration.split(':')[0]+'H'+package_meta.duration.split(':')[1]+'M'\
                         +package_meta.duration.split(':')[2]+'S'
        if sitemap.sitemap == False:
            return errorchecker.not_supported_asset_type(package_main.adi_type)

        if 'VRP' in package_main.adi_type:
            movie_path = ""
            image_path = ""
        else:
            movie_path = movie_config.video_path
            image_path = movie_config.image_path

        values = []
        values.append({
            'title': package_meta.title,
            'providerid': package_main.provider_id,
            'assetid': package_main.original_timestamp,
            'provider_version': package_main.provider_version,
            'licensetime': package_offer.licenseEndTime,
            'offerStartDateTime': package_offer.offerStartTime,
            'offerEndDateTime': package_offer.offerEndTime,
            'multiformatid': package_main.multiformat_id,
            'subtitle_flag': package_meta.subtitle_flag,
            'par_rating': package_meta.par_rating,
            'audio_type': package_meta.audio_type,
            'frame_rate': package_meta.frame_rate,
            'btc_rating': package_meta.btc_rating,
            'runtime': package_meta.duration,
            'duration': asset_duration,
            'movie_url': package_media.movie_url,
            'movie_checksum': package_media.movie_checksum,
            'video_type': package_meta.video_type,
            'offer_type': package_offer.offer_type,
            'service_key': package_offer.service_key,
            'epgTime': package_offer.epgTime,
            'asset_syn': package_meta.synopsis,
            'production_year': package_meta.production_year,
            'movie_path': movie_path,
            'image_path': image_path,
        })

        template = render_template(sitemap.sitemap, values=values)
        response = make_response(template)
        response.headers['Content-Type'] = 'application/xml'

        return response

    except:
        return errorchecker.asset_not_found_id(assetId)

def download_est_episode(assetId):
    movie_path = movie_config.video_path
    image_path = movie_config.image_path
    package_main = ADI_main.query.filter_by(assetId=assetId).first()
    package_meta = ADI_metadata.query.filter_by(assetId=assetId).first()
    package_offer = ADI_offer.query.filter_by(assetId=assetId).first()
    package_media = ADI_media.query.filter_by(assetId=assetId).first()
    package_group = ADI_EST_Show.query.filter_by(assetId=assetId).first()
    sitemap.sitemap_entry_boxset(package_main.adi_type, package_group.show_type)
    values = []

    show_group = ADI_EST_Show.query.filter_by(assetId=package_group.parent_group_id).first()
    show_metadata = ADI_metadata.query.filter_by(assetId=show_group.parent_group_id).first()
    if package_group.show_type == 'Movie BS':
        deal_sub = 'M/B'
        genre = '6:4'
    else:
        deal_sub = 'E/B'
        genre = '3:4'
    values.append({
        'episode_title': package_meta.title,
        'show_title': show_metadata.title,
        'season_number': package_group.season_number,
        'episode_number': package_group.episode_number,
        'deal_sub': deal_sub,
        'genre': genre,
        'providerid': package_main.provider_id,
        'assetid': package_main.assetId,
        'provider_version': package_main.provider_version,
        'licensetime': package_offer.licenseEndTime,
        'offerStartDateTime': package_offer.offerStartTime,
        'offerEndDateTime': package_offer.offerEndTime,
        'par_rating': package_meta.par_rating,
        'btc_rating': package_meta.btc_rating,
        'asset_syn': package_meta.synopsis,
        'movie_url': package_media.movie_url,
        'movie_checksum': package_media.movie_checksum,
        'movie_path': movie_path,
        'image_path': image_path,
        })

    template = render_template(sitemap.sitemap, values=values)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'

    return response

def download_est_season(assetId):
    package_main = ADI_main.query.filter_by(assetId=assetId).first()
    package_meta = ADI_metadata.query.filter_by(assetId=assetId).first()
    package_offer = ADI_offer.query.filter_by(assetId=assetId).first()
    package_group = ADI_EST_Show.query.filter_by(assetId=assetId).first()
    sitemap.sitemap_entry_boxset(package_main.adi_type, package_group.show_type)
    values = []
    if package_group.show_type == 'Movie BS':
        deal_sub = 'M/B'
        genre = '6:4'
    else:
        deal_sub = 'E/B'
        genre = '3:4'
    values.append({
        'title': package_meta.title,
        'season_number': package_group.season_number,
        'deal_sub': deal_sub,
        'genre': genre,
        'providerid': package_main.provider_id,
        'assetid': package_main.assetId,
        'provider_version': package_main.provider_version,
        'licensetime': package_offer.licenseEndTime,
        'par_rating': package_meta.par_rating,
        'btc_rating': package_meta.btc_rating,
        'asset_syn': package_meta.synopsis,
        })

    episodelist = []
    for package in ADI_EST_Show.query.filter(ADI_EST_Show.parent_group_id == assetId).all():
        episode_main = ADI_main.query.filter_by(assetId=package.assetId).first()
        episode_group = ADI_EST_Show.query.filter_by(assetId=package.assetId).first()
        episodelist.append({
            'episode_providerid': episode_main.provider_id,
            'episode_assetId': episode_main.assetId,
            'episode_number': episode_group.episode_number,
        })


    template = render_template(sitemap.sitemap, values=values, episodelist=episodelist)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'

    return response

def download_est_show(assetId):
    image_path = movie_config.image_path
    package_main = ADI_main.query.filter_by(assetId=assetId).first()
    package_meta = ADI_metadata.query.filter_by(assetId=assetId).first()
    package_offer = ADI_offer.query.filter_by(assetId=assetId).first()
    package_group = ADI_EST_Show.query.filter_by(assetId=assetId).first()
    sitemap.sitemap_entry_boxset(package_main.adi_type, package_group.show_type)
    values = []
    if package_group.show_type == 'Movie BS':
        deal_sub = 'M/B'
        genre = '6:4'
    else:
        deal_sub = 'E/B'
        genre = '3:4'
    values.append({
        'title': package_meta.title,
        'deal_sub': deal_sub,
        'genre': genre,
        'providerid': package_main.provider_id,
        'assetid': package_main.assetId,
        'provider_version': package_main.provider_version,
        'licensetime': package_offer.licenseEndTime,
        'par_rating': package_meta.par_rating,
        'btc_rating': package_meta.btc_rating,
        'asset_syn': package_meta.synopsis,
        'offerStartDateTime': package_offer.offerStartTime,
        'offerEndDateTime': package_offer.offerEndTime,
        'image_path': image_path,
        })

    seasonlist = []
    for package in ADI_EST_Show.query.filter(ADI_EST_Show.parent_group_id == assetId).all():
        season_main = ADI_main.query.filter_by(assetId=package.assetId).first()
        season_group = ADI_EST_Show.query.filter_by(assetId=package.assetId).first()
        seasonlist.append({
            'season_providerid': season_main.provider_id,
            'season_assetid': season_main.assetId,
            'season_number': season_group.season_number,
        })


    template = render_template(sitemap.sitemap, values=values, seasonlist=seasonlist)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'

    return response


def get_asset_data(assetId):
    adi_metadata = {}
    adi_metadata['packages'] = {}
    package = ADI_metadata.query.filter_by(assetId=assetId).first()
    if not package:
        return errorchecker.asset_not_found_id(assetId)

    adi_metadata['packages']['assetId'] = package.assetId
    adi_metadata['packages']['title'] = package.title
    adi_metadata['packages']['synopsis'] = package.synopsis
    adi_metadata['packages']['audio_type'] = package.audio_type
    adi_metadata['packages']['Parental Rating'] = package.par_rating
    adi_metadata['packages']['CA/BTC Rating'] = package.btc_rating
    adi_metadata['packages']['Subtitle'] = package.subtitle_flag

    json_data = dumps(adi_metadata)
    return response.asset_retrieve(json_data)

def get_asset_video(assetId):
    adi_metadata = {}
    adi_metadata['packages'] = {}
    package = ADI_metadata.query.filter_by(assetId=assetId).first()
    package_media = ADI_media.query.filter_by(assetId=assetId).first()
    if not package:
        return errorchecker.asset_not_found_id(assetId)

    adi_metadata['packages']['assetId'] = package.assetId
    adi_metadata['packages']['title'] = package.title
    adi_metadata['packages']['Movie File'] = package_media.movie_url
    adi_metadata['packages']['Movie Checksum'] = package_media.movie_checksum

    json_data = dumps(adi_metadata)
    return response.asset_retrieve(json_data)

def post_adi_endpoint():
    my_filename = movie_config.premium_vrp_dir+'/ADI.xml'
    ts = time.time()
    conversationId = datetime.datetime.fromtimestamp(ts).strftime('%d%H%M%S')
    environment = request.form.get('environment')
    params.environment_entry(environment)
    assetId = request.form.get('assetId')
    source = request.form.get('source')
    get_adi_url = 'http://localhost:5000/get_adi/' + assetId
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
        post_response['Message'] = 'AssetID: ' + assetId + ' ingested successfully'
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
        post_response['Message'] = 'Error connecting to Endpoint: ' + endpoint_url
        post_response['ConversationId'] = conversationId

    json_data = dumps(post_response)
    return response.asset_retrieve(json_data)