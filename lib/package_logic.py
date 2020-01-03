from flask import Blueprint
from . import movie_config
from . import errorchecker

main = Blueprint('main', __name__, static_url_path='', static_folder='../created_adi/', template_folder='../templates')


def sitemap_entry(asset_type, subtitle_flag):
    if subtitle_flag == 'true':
        if (asset_type == 'PREMIUM VOD') or (asset_type == 'SUBSCRIPTION VOD') or (asset_type == 'RENTAL'):
            return 'VOD_SINGLE_TITLE.xml'
        elif (asset_type == 'EST SINGLE TITLE'):
            return 'EST_SINGLE_TITLE.xml'
        elif (asset_type == 'CATCHUP'):
            return 'CUTV.xml'
        else:
            return False
    elif subtitle_flag == 'false':
        if (asset_type == 'PREMIUM VOD') or (asset_type == 'SUBSCRIPTION VOD') or (asset_type == 'RENTAL'):
            return 'VOD_SINGLE_TITLE_NOSUB.xml'
        elif (asset_type == 'EST SINGLE TITLE'):
            return 'EST_SINGLE_TITLE.xml'
        elif (asset_type == 'CATCHUP'):
            return 'CUTV.xml'
        else:
            return False
    elif (asset_type == 'est_show') or (asset_type == 'est_season') or (asset_type == 'est_episode'):
        return True
    else:
        return False


def sitemap_entry_boxset(asset_type):
    if (asset_type == 'est_show'):
        return 'EST_SHOW.xml'
    elif (asset_type == 'est_season'):
        return 'EST_SEASON.xml'
    elif (asset_type == 'est_episode'):
        return 'EST_EPISODE.xml'
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


def provider_version_entry(provider_version):
    if provider_version != "":
        return provider_version
    else:
        return '1'


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


def subtitle_entry(subtitle_flag):
    if subtitle_flag != "":
        return subtitle_flag
    else:
        return 'false'


def est_show_provider(show_type):
    if show_type == 'Movie BS':
        return 'est__movieboxset_hd'
    else:
        return 'est__tvboxset_hd'


def est_episode_provider(show_type):
    if show_type == 'Movie BS':
        return 'est__moviebstitle_hd'
    else:
        return 'est__tvepisode_hd'


def est_episode_title(show_type, title):
    if show_type == 'Movie BS':
        return title + ': Movie: '
    else:
        return title + ': Episode: '


def est_season_episode_count_entry(season_episode_count):
    if season_episode_count != "":
        return season_episode_count
    else:
        return '1'
