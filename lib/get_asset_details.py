from flask import Blueprint, render_template, make_response, request
from .models import ADI_main, ADI_media, ADI_metadata, ADI_offer, ADI_EST_Show, ADI_INGEST_HISTORY, MEDIA_DEFAULT, EST_PO
from . import movie_config
from .sitemap_create import sitemap_mapper
from bson.json_util import dumps
from . import response
import datetime, time
from .metadata_params import metadata_default_params
from .load_adi_logic import adi_package_logic
from . import errorchecker
import requests
import os
from . import db
path_to_script = os.path.dirname(os.path.abspath(__file__))
params = metadata_default_params()
sitemap = sitemap_mapper()
adicreate = adi_package_logic()
UPLOAD_DIRECTORY = movie_config.premium_vrp_dir

main = Blueprint('main', __name__, static_url_path='', static_folder='../premium_files/', template_folder='../templates')

def download_title(assetId):
    try:
        package_main = ADI_main.query.filter_by(assetId=assetId).first()
        package_meta = ADI_metadata.query.filter_by(assetId=assetId).first()
        package_offer = ADI_offer.query.filter_by(assetId=assetId).first()
        package_media = ADI_media.query.filter_by(assetId=assetId).first()
        sitemap.sitemap_entry(package_main.adi_type)
        adicreate.duration_calc(package_meta.duration)
        adicreate.path_builder(package_main.adi_type, assetId)
        adicreate.dpl_midroll_calc(package_main.adi_type, package_meta.total_asset_parts)
        adicreate.term_type_generate(package_main.adi_type)

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
            'par_rating': package_meta.par_rating,
            'audio_type': package_meta.audio_type,
            'frame_rate': package_meta.frame_rate,
            'btc_rating': package_meta.btc_rating,
            'runtime': package_meta.duration,
            'duration': adicreate.asset_duration,
            'movie_url': package_media.movie_url,
            'movie_checksum': package_media.movie_checksum,
            'video_type': package_meta.video_type,
            'offer_type': package_offer.offer_type,
            'asset_syn': package_meta.synopsis,
            'production_year': package_meta.production_year,
            'genre': package_meta.genre,
            'movie_path': adicreate.movie_path,
            'image_path': adicreate.image_path,
        })

        media_items = []
        media_items.append({
            'trailer_url': package_media.trailer_url,
            'trailer_checksum': package_media.trailer_checksum,
            'image1': package_media.image_url_1,
            'image2': package_media.image_url_2,
            'image3': package_media.image_url_3,
            'image4': package_media.image_url_4,
            'image5': package_media.image_url_5,
            'image6': package_media.image_url_6,
            'image1_checksum': package_media.image_checksum_1,
            'image2_checksum': package_media.image_checksum_2,
            'image3_checksum': package_media.image_checksum_3,
            'image4_checksum': package_media.image_checksum_4,
            'image5_checksum': package_media.image_checksum_5,
            'image6_checksum': package_media.image_checksum_6,
        })

        vodextensions = []
        vodextensions.append({
            'vod_deal_sub': 'M/N',
        })
        cutv = []
        cutv.append({
            'service_key': package_offer.service_key,
            'epgTime': package_offer.epgTime
        })
        terms = []
        terms.append({
            'term_type': adicreate.term_type,
        })
        episodes = []
        episodes.append({
            'svod_episode_name': package_meta.svod_episode_name,
            'svod_episode_number': package_meta.svod_episode_number,
            'svod_season_number': package_meta.svod_season_number,
            'svod_total_episodes': package_meta.svod_total_episodes,
        })
        subtitle = []
        subtitle.append({
            'subtitle_flag': package_meta.subtitle_flag,
        })

        if 'DPL' in package_main.adi_type:
            dpl_base = []
            dpl_base.append({
                'dpl_template': package_meta.dpl_template,
                'mid_rolls': adicreate.dpl_mid_rolls,
            })

            dpl_items = []
            for parts in range(1, int(package_meta.total_asset_parts) + 1):
                dpl_items.append({
                    'part_no': parts,
                })

        if 'EPISODE' not in package_main.adi_type and 'CATCHUP' not in package_main.adi_type:
            if 'DPL' not in package_main.adi_type and package_meta.subtitle_flag == 'true':
                template = render_template(sitemap.sitemap, values=values, vodextensions=vodextensions, terms=terms,
                                           subtitle=subtitle, media_items=media_items)
            elif 'DPL' not in package_main.adi_type and package_meta.subtitle_flag == 'false':
                template = render_template(sitemap.sitemap, values=values, vodextensions=vodextensions, terms=terms,
                                           media_items=media_items)
            else:
                template = render_template(sitemap.sitemap, values=values, vodextensions=vodextensions, terms=terms,
                                           dpl_items=dpl_items, dpl_base=dpl_base, media_items=media_items)
        elif 'EPISODE' not in package_main.adi_type and 'CATCHUP' in package_main.adi_type:
            if 'DPL' not in package_main.adi_type:
                template = render_template(sitemap.sitemap, values=values, terms=terms, cutv=cutv,
                                           media_items=media_items)
            else:
                template = render_template(sitemap.sitemap, values=values, terms=terms, dpl_items=dpl_items,
                                           dpl_base=dpl_base, cutv=cutv, media_items=media_items)
        elif 'EPISODE' in package_main.adi_type and 'CATCHUP' not in package_main.adi_type:
            if 'DPL' not in package_main.adi_type:
                template = render_template(sitemap.sitemap, values=values, episodes=episodes, terms=terms,
                                           media_items=media_items)
            else:
                template = render_template(sitemap.sitemap, values=values, episodes=episodes, terms=terms,
                                           dpl_items=dpl_items, dpl_base=dpl_base, media_items=media_items)
        elif 'EPISODE' in package_main.adi_type and 'CATCHUP' in package_main.adi_type:
            if 'DPL' not in package_main.adi_type:
                template = render_template(sitemap.sitemap, values=values, episodes=episodes, terms=terms,
                                           cutv=cutv, media_items=media_items)
            else:
                template = render_template(sitemap.sitemap, values=values, episodes=episodes, terms=terms, cutv=cutv,
                                           dpl_items=dpl_items, dpl_base=dpl_base, media_items=media_items)

        response = make_response(template)
        response.headers['Content-Type'] = 'application/xml'
        return response

    except:
        return errorchecker.internal_server_error()




def download_est_episode(assetId):
    package_main = ADI_main.query.filter_by(assetId=assetId).first()
    package_meta = ADI_metadata.query.filter_by(assetId=assetId).first()
    package_offer = ADI_offer.query.filter_by(assetId=assetId).first()
    package_media = ADI_media.query.filter_by(assetId=assetId).first()
    package_group = ADI_EST_Show.query.filter_by(assetId=assetId).first()
    sitemap.sitemap_entry_boxset(package_main.adi_type, package_group.show_type)
    adicreate.path_builder(package_main.adi_type, assetId)
    values = []

    show_group = ADI_EST_Show.query.filter_by(assetId=package_group.parent_group_id).first()
    show_metadata = ADI_metadata.query.filter_by(assetId=show_group.parent_group_id).first()
    if package_group.show_type == 'Movie BS':
        deal_sub = 'M/B'
        genre = movie_config.default_movie_genre
    else:
        deal_sub = 'E/B'
        genre = movie_config.default_episode_genre
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
        'movie_path': adicreate.movie_path,
        'image_path': adicreate.image_path,
        })

    media_items = []
    media_items.append({
        'image1': package_media.image_url_1,
        'image2': package_media.image_url_2,
        'image3': package_media.image_url_3,
        'image4': package_media.image_url_4,
        'image1_checksum': package_media.image_checksum_1,
        'image2_checksum': package_media.image_checksum_2,
        'image3_checksum': package_media.image_checksum_3,
        'image4_checksum': package_media.image_checksum_4,
    })

    template = render_template(sitemap.sitemap, values=values, media_items=media_items)
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
    package_main = ADI_main.query.filter_by(assetId=assetId).first()
    package_meta = ADI_metadata.query.filter_by(assetId=assetId).first()
    package_offer = ADI_offer.query.filter_by(assetId=assetId).first()
    package_group = ADI_EST_Show.query.filter_by(assetId=assetId).first()
    package_media = ADI_media.query.filter_by(assetId=assetId).first()
    sitemap.sitemap_entry_boxset(package_main.adi_type, package_group.show_type)
    adicreate.path_builder(package_main.adi_type, assetId)
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
        # 'offerStartDateTime': package_offer.offerStartTime,
        # 'offerEndDateTime': package_offer.offerEndTime,
        'image_path': adicreate.image_path,
        })

    media_items = []
    media_items.append({
         'image1': package_media.image_url_1,
         'image2': package_media.image_url_2,
         'image3': package_media.image_url_3,
         'image4': package_media.image_url_4,
         'image1_checksum': package_media.image_checksum_1,
         'image2_checksum': package_media.image_checksum_2,
         'image3_checksum': package_media.image_checksum_3,
         'image4_checksum': package_media.image_checksum_4,
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

    purchase_options = []
    for package in EST_PO.query.filter(EST_PO.assetId == assetId).all():
        po = EST_PO.query.filter_by(poption_Id=package.poption_Id).first()
        purchase_options.append({
            'option_id': po.poption_Id,
            'media_type': po.poption_media_type,
            'media_filter': po.poption_media_filter,
            'po_end': package_offer.offerEndTime,
            'uk_std_price': po.uk_std_price,
            'uk_vip_price': po.uk_vip_price,
            'il_std_price': po.il_std_price,
            'il_vip_price': po.il_vip_price,

        })

    est_offers = []
    for offers in ADI_offer.query.filter(ADI_offer.assetId == assetId).all():
        offeritem = ADI_offer.query.filter_by(est_offerId=offers.est_offerId).first()
        est_offers.append({
            'offer_id': offeritem.est_offerId,
            'offerEndDateTime': offeritem.offerEndTime,
            'offerStartDateTime': offeritem.offerStartTime,
            'offer_type': offeritem.offer_type,
            'order_type': offeritem.est_order_type,
        })


    template = render_template(sitemap.sitemap, values=values, seasonlist=seasonlist, media_items=media_items,
                               purchase_options=purchase_options, est_offers=est_offers)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'

    return response


def download_est_single_title(assetId):
    try:
        package_main = ADI_main.query.filter_by(assetId=assetId).first()
        package_meta = ADI_metadata.query.filter_by(assetId=assetId).first()
        package_offer = ADI_offer.query.filter_by(assetId=assetId).first()
        package_media = ADI_media.query.filter_by(assetId=assetId).first()
        sitemap.sitemap_entry_est_title(package_main.adi_type)
        adicreate.duration_calc(package_meta.duration)
        adicreate.path_builder(package_main.adi_type, assetId)
        adicreate.term_type_generate(package_main.adi_type)

        values = []
        values.append({
            'title': package_meta.title,
            'providerid': package_main.provider_id,
            'assetid': package_main.original_timestamp,
            'provider_version': package_main.provider_version,
            'licensetime': package_offer.licenseEndTime,
            'par_rating': package_meta.par_rating,
            'audio_type': package_meta.audio_type,
            'frame_rate': package_meta.frame_rate,
            'btc_rating': package_meta.btc_rating,
            'runtime': package_meta.duration,
            'duration': adicreate.asset_duration,
            'movie_url': package_media.movie_url,
            'movie_checksum': package_media.movie_checksum,
            'video_type': package_meta.video_type,
            'offer_type': package_offer.offer_type,
            'asset_syn': package_meta.synopsis,
            'production_year': package_meta.production_year,
            'movie_path': adicreate.movie_path,
            'image_path': adicreate.image_path,
        })


        media_items = []
        media_items.append({
            'trailer_url': package_media.trailer_url,
            'trailer_checksum': package_media.trailer_checksum,
            'image1': package_media.image_url_1,
            'image2': package_media.image_url_2,
            'image3': package_media.image_url_3,
            'image4': package_media.image_url_4,
            'image5': package_media.image_url_5,
            'image6': package_media.image_url_6,
            'image1_checksum': package_media.image_checksum_1,
            'image2_checksum': package_media.image_checksum_2,
            'image3_checksum': package_media.image_checksum_3,
            'image4_checksum': package_media.image_checksum_4,
            'image5_checksum': package_media.image_checksum_5,
            'image6_checksum': package_media.image_checksum_6,
        })

        purchase_options = []
        for package in EST_PO.query.filter(EST_PO.assetId == assetId).all():
            po = EST_PO.query.filter_by(poption_Id=package.poption_Id).first()
            purchase_options.append({
                'option_id': po.poption_Id,
                'media_type': po.poption_media_type,
                'media_filter': po.poption_media_filter,
                'po_end': package_offer.offerEndTime,
                'uk_std_price': po.uk_std_price,
                'uk_vip_price': po.uk_vip_price,
                'il_std_price': po.il_std_price,
                'il_vip_price': po.il_vip_price,

            })

        est_offers = []
        for offers in ADI_offer.query.filter(ADI_offer.assetId == assetId).all():
            offeritem = ADI_offer.query.filter_by(est_offerId=offers.est_offerId).first()
            est_offers.append({
                'offer_id': offeritem.est_offerId,
                'offerEndDateTime': offeritem.offerEndTime,
                'offerStartDateTime': offeritem.offerStartTime,
                'offer_type': offeritem.offer_type,
                'order_type': offeritem.est_order_type,
            })


        template = render_template(sitemap.sitemap, values=values, media_items=media_items, est_offers=est_offers,
                                   purchase_options=purchase_options)
        response = make_response(template)
        response.headers['Content-Type'] = 'application/xml'
        return response

    except:
        return errorchecker.internal_server_error()


def get_asset_data(assetId):
    adi_metadata = {}
    adi_metadata['packages'] = {}
    package = ADI_metadata.query.filter_by(assetId=assetId).first()
    package_media = ADI_media.query.filter_by(assetId=assetId).first()
    if not package:
        return errorchecker.asset_not_found_id(assetId)

    adi_metadata['packages']['assetId'] = package.assetId
    adi_metadata['packages']['title'] = package.title
    adi_metadata['packages']['synopsis'] = package.synopsis
    adi_metadata['packages']['audio_type'] = package.audio_type
    adi_metadata['packages']['Parental Rating'] = package.par_rating
    adi_metadata['packages']['CA/BTC Rating'] = package.btc_rating
    adi_metadata['packages']['Subtitle'] = package.subtitle_flag
    adi_metadata['packages']['Movie File'] = package_media.movie_url
    adi_metadata['packages']['Movie Checksum'] = package_media.movie_checksum

    json_data = dumps(adi_metadata)
    return response.asset_retrieve(json_data)

def get_est_offers(assetId):
    adi_offers = {}
    adi_offers['offers'] = []
    package_check = ADI_main.query.filter_by(assetId=assetId).first()
    if (package_check.adi_type == 'EST SINGLE TITLE') or (package_check.adi_type == 'est_show'):
        for package in ADI_offer.query.filter(ADI_offer.assetId == assetId).all():
            package_offer = ADI_offer.query.filter_by(est_offerId=package.est_offerId).first()
            package_meta = ADI_metadata.query.filter_by(assetId=package.assetId).first()
            adi_offers['offers'].append({
                'title': package_meta.title,
                'assetId': package.assetId,
                'offer_type': package_offer.offer_type,
                'est_offer_id': package_offer.est_offerId,
                'est_order_type': package_offer.est_order_type,
                'offerStartTime': package_offer.offerStartTime,
                'offerEndTime': package_offer.offerEndTime,
                })


        adi_offers['total'] = ADI_offer.query.filter(ADI_offer.assetId == assetId).count()
        if adi_offers['total'] == 0:  # If no countries found in the continent
            return errorchecker.no_assets_in_db()
        else:
            json_data = dumps(adi_offers)

        return response.asset_retrieve(json_data)

    else:
        return errorchecker.not_est_offer(assetId)


def get_default_config():
    default_config = {}
    default_config['config'] = {}
    config_data = MEDIA_DEFAULT.query.first()
    default_config['config']['Video Path'] = config_data.default_video_path
    default_config['config']['Image Path'] = config_data.default_image_path
    default_config['config']['HD Video'] = config_data.hd_movie_file
    default_config['config']['SD Video'] = config_data.title_movie_file
    default_config['config']['4K Video'] = config_data.sdr_movie_file
    default_config['config']['HDR Video'] = config_data.hdr_movie_file
    default_config['config']['DPL Video'] = config_data.dpl_movie_file
    default_config['config']['EST Video'] = config_data.est_movie_file
    default_config['config']['Trailer'] = config_data.trailer_file
    default_config['config']['Standard Image'] = config_data.standard_image_file_prefix
    default_config['config']['DPL Image'] = config_data.dpl_image_file_prefix

    json_data = dumps(default_config)
    return response.asset_retrieve(json_data)



def post_adi_endpoint():
    ts = time.time()
    conversationId = datetime.datetime.fromtimestamp(ts).strftime('%d%H%M%S')
    ingest_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S %d/%m/%Y')
    environment = request.form.get('environment')
    params.environment_entry(environment)
    source = request.form.get('source')
    endpoint_url = params.environment_url + 'source=' + source + '&conversationId=' + conversationId
    headers = {'Content-type': 'text/xml; charset=UTF-8'}
    if 'file' not in request.files and request.form.get('assetId') == "":
        return errorchecker.input_missing('AssetId or ADI Filename')
    elif request.form.get('assetId') == "":
        file = request.files['file']
        if file.filename == '':
            return errorchecker.input_missing('AssetId or ADI Filename')
        else:
            file.save(os.path.join(UPLOAD_DIRECTORY, file.filename))
            my_filename = movie_config.premium_vrp_dir + '/' + file.filename
            data = open(my_filename, 'rb').read()
            post_response = {}
            try:
                response_post_adi = requests.post(url=endpoint_url, data=data, headers=headers)
                post_response['Status'] = '200'
                post_response['Message'] = file.filename + ' ingested successfully'
                post_response['Endpoint'] = endpoint_url
                post_response['ConversationId'] = conversationId
                post_response['Endpoint_Response'] = response_post_adi.text
            except:
                post_response['Status'] = '404'
                post_response['Message'] = 'Error connecting to Endpoint: ' + endpoint_url
                post_response['ConversationId'] = conversationId

            json_data = dumps(post_response)
            return response.asset_retrieve(json_data)


    else:
        my_filename = movie_config.premium_vrp_dir+'/ADI.xml'
        assetId = request.form.get('assetId')
        try:
            package = ADI_main.query.filter_by(assetId=assetId).first()
            assetId_db = package.assetId
            get_adi_url = 'http://localhost:5000/get_adi/' + assetId
            response_adi = requests.get(url=get_adi_url)
            with open(my_filename, 'w') as f:
                f.write(response_adi.text)
            data = open(my_filename, 'rb').read()
            post_response = {}
            try:
                response_post_adi = requests.post(url=endpoint_url, data=data, headers=headers)
                post_response['Status'] = '200'
                post_response['Message'] = 'AssetID: ' + assetId_db + ' ingested successfully'
                post_response['Endpoint'] = endpoint_url
                post_response['ConversationId'] = conversationId
                post_response['Endpoint_Response'] = response_post_adi.text
                package = ADI_main.query.filter_by(assetId=assetId).first()
                ingest_response = ADI_INGEST_HISTORY(assetId=assetId, provider_version=package.provider_version,
                                                     environment=environment, conversationId=conversationId,
                                                     ingest_timestamp=ingest_timestamp)
                db.session.add(ingest_response)
                db.session.commit()
            except:
                post_response['Status'] = '404'
                post_response['Message'] = 'Error connecting to Endpoint: ' + endpoint_url
                post_response['ConversationId'] = conversationId

            json_data = dumps(post_response)
            return response.asset_retrieve(json_data)

        except:
            return errorchecker.asset_not_found_id(assetId)
