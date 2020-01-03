from flask import request
from .models import ADI_main, ADI_metadata, ADI_offer, ADI_media, ADI_EST_Show
from . import errorchecker
import urllib.parse
from bson.json_util import dumps
from . import response
from sqlalchemy import or_, and_

def search_by_title():
    title = request.form.get('Title')
    title_uncoded = urllib.parse.unquote_plus(title)
    adi_data = {}
    adi_data['packages'] = []
    search = "{}%".format(title_uncoded)
    for package in ADI_metadata.query.filter(or_(ADI_metadata.title.like(search)), (ADI_metadata.title_filter == 'true')).all():
        package_main = ADI_main.query.filter_by(assetId=package.assetId).first()
        package_offer = ADI_offer.query.filter_by(assetId=package.assetId).first()
        adi_data['packages'].append({
            'title': package.title,
            'assetId': package.assetId,
            'package_type': package_main.adi_type,
            'providerVersionNum': package_main.provider_version,
            'providerId': package_main.provider_id,
            'offerEndDateTime': package_offer.offerEndTime,
            'multiformat_id': package_main.multiformat_id
        })

    adi_data['total'] = ADI_metadata.query.filter(or_(ADI_metadata.title.like(search)), (ADI_metadata.title_filter == 'true')).count()

    if adi_data['total'] == 0:  # If no ADI found
        return errorchecker.not_matched_criteria()
    else:
        json_data = dumps(adi_data)

    return response.asset_retrieve(json_data)


def search_all_packages():
    adi_data = {}
    adi_data['packages'] = []
    for package in ADI_main.query.filter(or_(ADI_main.adi_type != 'est_episode'), (ADI_main.adi_type != 'est_season')).all():
        package_offer = ADI_offer.query.filter_by(assetId=package.assetId).first()
        package_meta = ADI_metadata.query.filter_by(assetId=package.assetId).first()
        adi_data['packages'].append({
            'title': package_meta.title,
            'assetId': package.assetId,
            'package_type': package.adi_type,
            'providerVersionNum': package.provider_version,
            'providerId': package.provider_id,
            'offerEndDateTime': package_offer.offerEndTime,
            'multiformat_id': package.multiformat_id
        })

    adi_data['total'] = ADI_main.query.filter(or_(ADI_main.adi_type != 'est_episode'), (ADI_main.adi_type != 'est_season')).count()

    if adi_data['total'] == 0:  # If no countries found in the continent
        return errorchecker.no_assets_in_db()
    else:
        json_data = dumps(adi_data)

    return response.asset_retrieve(json_data)


def search_est_assets():
    title = request.form.get('Title')
    title_uncoded = urllib.parse.unquote_plus(title)
    adi_data = {}
    adi_data['packages'] = []
    search = "{}%".format(title_uncoded)
    for package in ADI_EST_Show.query.filter(ADI_EST_Show.title.like(search)).all():
        package_offer = ADI_offer.query.filter_by(assetId=package.assetId).first()
        package_main = ADI_main.query.filter_by(assetId=package.assetId).first()
        package_group = ADI_EST_Show.query.filter_by(assetId=package.assetId).first()
        adi_data['packages'].append({
            'title': package.title,
            'assetId': package.assetId,
            'package_type': package_main.adi_type,
            'providerVersionNum': package_main.provider_version,
            'providerId': package_main.provider_id,
            'offerEndDateTime': package_offer.offerEndTime,
            'parent_group_id': package_group.parent_group_id,
            'no_of_seasons': package_group.no_of_seasons,
            'season_number': package_group.season_number,
            'no_of_episodes': package_group.no_of_episodes,
            'episode_number': package_group.episode_number,
        })

    adi_data['total'] = ADI_EST_Show.query.filter(ADI_EST_Show.title.like(search)).count()

    if adi_data['total'] == 0:  # If no countries found in the continent
        return errorchecker.no_assets_in_db()
    else:
        json_data = dumps(adi_data)

    return response.asset_retrieve(json_data)