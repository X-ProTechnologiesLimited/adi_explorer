from flask import request
from .models import ADI_main, ADI_metadata, ADI_offer, ADI_media
from . import errorchecker
import urllib.parse
from bson.json_util import dumps
from . import response

def search_by_title():
    title = request.form.get('Title')
    title_uncoded = urllib.parse.unquote_plus(title)
    adi_data = {}
    adi_data['packages'] = []
    search = "{}%".format(title_uncoded)
    for package in ADI_metadata.query.filter(ADI_metadata.title.like(search)).all():
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

    adi_data['total'] = ADI_metadata.query.filter(ADI_metadata.title.like(search)).count()

    if adi_data['total'] == 0:  # If no ADI found
        return errorchecker.not_matched_criteria()
    else:
        json_data = dumps(adi_data, sort_keys=True)

    return response.asset_retrieve(json_data)


def search_all_packages():
    adi_data = {}
    adi_data['packages'] = []
    for package in ADI_main.query.all():
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

    adi_data['total'] = ADI_main.query.count()

    if adi_data['total'] == 0:  # If no countries found in the continent
        return errorchecker.no_assets_in_db()
    else:
        json_data = dumps(adi_data, sort_keys=True)

    return response.asset_retrieve(json_data)