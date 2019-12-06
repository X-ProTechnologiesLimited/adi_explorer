from flask import Blueprint, render_template, make_response
from .models import ADI_META
from . import errorchecker
from . import movie_config

main = Blueprint('main', __name__, static_url_path='', static_folder='../created_adi/', template_folder='../templates')

def sitemap_entry(asset_type, subtitle_flag):
    if asset_type == 'EST SINGLE TITLE':
        return 'EST_SINGLE_TITLE.xml'
    elif asset_type == 'PREMIUM VOD' and subtitle_flag == 'true':
        return 'PREMVOD.xml'
    elif asset_type == 'PREMIUM VOD' and subtitle_flag == 'false':
        return 'PREMVOD_NOSUB.xml'
    else:
        return False


def multiformat_entry(multiformat_id, asset_timestamp):
    if multiformat_id != "":
        return multiformat_id
    else:
        return 'BSKYPR' + asset_timestamp


def movie_file_entry(provider_id):
    if 'hdr' in provider_id:
        return movie_config.hdr_movie_file
    elif '4k' in provider_id:
        return movie_config.sdr_movie_file
    elif 'est' in provider_id:
        return movie_config.est_movie_file
    elif 'hd.' in  provider_id:
        return movie_config.hd_movie_file
    else:
        return movie_config.title_movie


def movie_checksum_entry(provider_id):
    if 'hdr' in provider_id:
        return movie_config.hdr_movie_checksum
    elif '4k' in provider_id:
        return movie_config.sdr_movie_checksum
    elif 'est' in provider_id:
        return movie_config.est_movie_checksum
    elif 'hd.' in  provider_id:
        return movie_config.hd_movie_checksum
    else:
        return movie_config.title_checksum


def download_adi_package(assetId):
    try:
        package = ADI_META.query.filter_by(assetId=assetId).first()
        sitemap = sitemap_entry(package.adi_type, package.subtitle_flag)
        if sitemap == False:
            return errorchecker.not_supported_asset_type(package.adi_type)

        values = []
        values.append({
            'title': package.title,
            'providerid': package.provider_id,
            'assetid': package.original_timestamp,
            'provider_version': package.provider_version,
            'licensetime': package.licenseEndTime,
            'offerStartDateTime': package.offerStartTime,
            'offerEndDateTime': package.offerEndTime,
            'multiformatid': package.multiformat_id,
            'subtitle_flag': package.subtitle_flag,
            'par_rating': package.par_rating,
            'audio_type': package.audio_type,
            'frame_rate': package.frame_rate,
            'btc_rating': package.btc_rating,
            'movie_url': package.movie_url,
            'movie_checksum': package.movie_checksum,
        })

        template = render_template(sitemap, values=values)
        response = make_response(template)
        response.headers['Content-Type'] = 'application/xml'

        return response

    except:
        return errorchecker.asset_not_found_id(assetId)