from flask import Blueprint, render_template, make_response, send_file
from .models import ADI_META
from . import errorchecker
from . import movie_config

main = Blueprint('main', __name__, static_url_path='', static_folder='../created_adi/', template_folder='../templates')

def sitemap_entry(asset_type, subtitle_flag):
    if subtitle_flag == 'true':
        if (asset_type == 'PREMIUM VOD') or (asset_type == 'SUBSCRIPTION VOD') or (asset_type == 'RENTAL'):
            return 'VOD_SINGLE_TITLE.xml'
        elif (asset_type == 'EST SINGLE TITLE'):
            return 'EST_SINGLE_TITLE.xml'
        else:
            return False
    elif subtitle_flag == 'false':
        if (asset_type == 'PREMIUM VOD') or (asset_type == 'SUBSCRIPTION VOD') or (asset_type == 'RENTAL'):
            return 'VOD_SINGLE_TITLE_NOSUB.xml'
        elif (asset_type == 'EST SINGLE TITLE'):
            return 'EST_SINGLE_TITLE.xml'
        else:
            return False
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
    elif ('hd.' in provider_id) or ('_hd' in provider_id):
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
    elif ('hd.' in provider_id) or ('_hd' in provider_id):
        return movie_config.hd_movie_checksum
    else:
        return movie_config.title_checksum


def video_type_entry(provider_id):
    if ('hdr' in provider_id) or ('4k' in provider_id) or ('hd.' in provider_id) or ('_hd' in provider_id):
        return 'true'
    else:
        return 'false'

def offer_type_entry(asset_type):
    if asset_type == 'SUBSCRIPTION VOD':
        return 'SVOD'
    else:
        return 'IPPR'

def synopsis_entry(synopsis, title):
    if synopsis != "":
        return synopsis
    else:
        return 'This is the synopsis of asset named: ' + title


def production_year_entry(production_year):
    if production_year != "":
        return production_year
    else:
        return '2000'

def btc_entry(ca_btc):
    if ca_btc != "":
        return ca_btc
    else:
        return 'U'

def par_rating_entry(par_rating):
    if par_rating != "":
        return par_rating
    else:
        return '1'

def audio_type_entry(audio_type):
    if audio_type != "":
        return audio_type
    else:
        return 'Dolby Digital'

def frame_rate_entry(frame_rate):
    if frame_rate != "":
        return frame_rate
    else:
        return '25'


def download_adi_package(assetId):
    try:
        package = ADI_META.query.filter_by(assetId=assetId).first()
        sitemap = sitemap_entry(package.adi_type, package.subtitle_flag)
        if sitemap == False:
            return errorchecker.not_supported_asset_type(package.adi_type)

        if package.adi_type == 'PREMIUM VOD':
            movie_path = ""
            image_path = ""
        else:
            movie_path = movie_config.video_path
            image_path = movie_config.image_path

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
            'video_type': package.video_type,
            'offer_type': package.offer_type,
            'asset_syn': package.synopsis,
            'production_year': package.production_year,
            'movie_path': movie_path,
            'image_path': image_path,
        })

        template = render_template(sitemap, values=values)
        response = make_response(template)
        response.headers['Content-Type'] = 'application/xml'

        return response

    except:
        return errorchecker.asset_not_found_id(assetId)