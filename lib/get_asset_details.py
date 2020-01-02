from flask import Blueprint, render_template, make_response
from .models import ADI_main, ADI_media, ADI_metadata, ADI_offer, ADI_EST_Show
from . import errorchecker
from . import movie_config
from . import package_logic
from bson.json_util import dumps
from . import response

main = Blueprint('main', __name__, static_url_path='', static_folder='../created_adi/', template_folder='../templates')



def download_title(assetId):
    try:
        package_main = ADI_main.query.filter_by(assetId=assetId).first()
        package_meta = ADI_metadata.query.filter_by(assetId=assetId).first()
        package_offer = ADI_offer.query.filter_by(assetId=assetId).first()
        package_media = ADI_media.query.filter_by(assetId=assetId).first()
        sitemap = package_logic.sitemap_entry(package_main.adi_type, package_meta.subtitle_flag)
        if sitemap == False:
            return errorchecker.not_supported_asset_type(package_main.adi_type)
        elif sitemap == True:
            return errorchecker.use_different_method(package_main.adi_type)

        if package_main.adi_type == 'PREMIUM VOD':
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

        template = render_template(sitemap, values=values)
        response = make_response(template)
        response.headers['Content-Type'] = 'application/xml'

        return response

    except:
        return errorchecker.asset_not_found_id(assetId)


def download_est(assetId):
    movie_path = movie_config.video_path
    image_path = movie_config.image_path
    package_main = ADI_main.query.filter_by(assetId=assetId).first()
    package_meta = ADI_metadata.query.filter_by(assetId=assetId).first()
    package_offer = ADI_offer.query.filter_by(assetId=assetId).first()
    package_media = ADI_media.query.filter_by(assetId=assetId).first()
    package_group = ADI_EST_Show.query.filter_by(assetId=assetId).first()
    sitemap = package_logic.sitemap_entry_boxset(package_main.adi_type)
    values = []
    if sitemap == False:
        return errorchecker.use_different_method(package_main.adi_type)

    if package_main.adi_type == 'est_episode':
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
            'movie_url': package_media.movie_url,
            'movie_checksum': package_media.movie_checksum,
            'movie_path': movie_path,
            'image_path': image_path,
            })

    elif package_main.adi_type == 'est_season':
        return errorchecker.not_implemented_yet()

    elif package_main.adi_type == 'est_show':
        return errorchecker.not_implemented_yet()

    template = render_template(sitemap, values=values)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'

    return response

    # except:
    #     return errorchecker.asset_not_found_id(assetId)

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