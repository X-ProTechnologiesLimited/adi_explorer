# Filename: lib/search.py
"""
Created on June 01, 2020

@author: Krishnendu Banerjee
@summary: This file holds the functions to perform different search assets in the local database
"""
import urllib.parse
from flask import request
from .models import ADI_main, ADI_metadata, ADI_offer, ADI_EST_Show, ADI_INGEST_HISTORY, MEDIA_LIBRARY
from . import errorchecker, response
from bson.json_util import dumps
from sqlalchemy import or_, and_

def search_by_title():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function to Search Assets by Title (Non-Case Sensitive) from Database
    :access: public.
    :return: retrieve the search response in JSON format
    """
    title = request.form.get('Title')
    title_uncoded = urllib.parse.unquote_plus(title) # Space and special character handling
    adi_data = []
    search = "%{}%".format(title_uncoded) # Pattern match with search criterion anywhere in title
    title_search = ADI_metadata.query.filter(or_(ADI_metadata.title.like(search)),
                                                  (ADI_metadata.title_filter == 'true')).count()
    id_search = ADI_main.query.filter(ADI_main.assetId == title).count()

    if title_search == 0 and id_search == 0:
        return errorchecker.not_matched_criteria()
    elif title_search == 0:
        matched_items = ADI_main.query.filter(ADI_main.assetId == title).all()

    elif id_search == 0:
        matched_items = ADI_metadata.query.filter(or_(ADI_metadata.title.like(search)),
                                                  (ADI_metadata.title_filter == 'true')).all()


    for package in matched_items:
        package_main = ADI_main.query.filter_by(assetId=package.assetId).first()
        package_offer = ADI_offer.query.filter_by(assetId=package.assetId).first()
        package_meta = ADI_metadata.query.filter_by(assetId=package.assetId).first()
        if 'est_show' in package_main.adi_type:
            title_link = f'<a style="font-weight:bold" href="/expand_show/{package_meta.title}"</a>{package_meta.title}'
        else:
            title_link = package_meta.title
        adi_data.append({
            'Select': f'<input type="radio" name="AssetId" value="{package.assetId}">',
            'Title': title_link,
            'AssetId': package.assetId,
            'Package type': package_main.adi_type,
            'Provider Version': package_main.provider_version,
            'ProviderId': package_main.provider_id,
            'Offer EndDateTime': package_offer.offerEndTime,
            'Multiformat id': package_main.multiformat_id,
        })
    json_data = dumps(adi_data, ensure_ascii=False)

    return response.asset_retrieve_form(json_data)



def search_all_packages():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function to Return all Assets in Database in JSON Format
    :access: public.
    :return: Return all assets in Database in JSON format
    """
    adi_data = []
    for package in ADI_main.query.filter(or_(ADI_main.adi_type != 'est_episode'), (ADI_main.adi_type != 'est_season')).\
            order_by(ADI_main.id.desc()).all():
        package_offer = ADI_offer.query.filter_by(assetId=package.assetId).first()
        package_meta = ADI_metadata.query.filter_by(assetId=package.assetId).first()
        if 'est_show' in package.adi_type:
            title_link = f'<a style="font-weight:bold" href="/expand_show/{package_meta.title}"</a>{package_meta.title}'
        else:
            title_link = package_meta.title
        adi_data.append({
            'Select': f'<input type="radio" name="AssetId" value="{package.assetId}">',
            'Title': title_link,
            'AssetId': package.assetId,
            'Package type': package.adi_type,
            'Provider Version': package.provider_version,
            'ProviderId': package.provider_id,
            'Offer EndDateTime': package_offer.offerEndTime,
            'Multiformat id': package.multiformat_id,
            'Content Marked': package.content_marker,
        })

    total = ADI_main.query.filter(or_(ADI_main.adi_type != 'est_episode'), (ADI_main.adi_type != 'est_season')).count()

    if total == 0:  # If no assets found in the database
        return errorchecker.no_assets_in_db()
    else:
        json_data = dumps(adi_data, ensure_ascii=False)

    return response.asset_retrieve_form(json_data)


def expand_est_show(title):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function to Search EST Assets by Title (Non-Case Sensitive) from Database
    :access: public.
    :return: Only EST Single Title, Episodes, Seasons and Box-Sets based on matched title
    """
    title_uncoded = urllib.parse.unquote_plus(title)
    adi_data = []
    search = "%{}%".format(title_uncoded)
    for package in ADI_EST_Show.query.filter(ADI_EST_Show.title.like(search)).\
            order_by(ADI_EST_Show.no_of_seasons.desc()).order_by(ADI_EST_Show.no_of_episodes.desc()).all():
        package_offer = ADI_offer.query.filter_by(assetId=package.assetId).first()
        package_main = ADI_main.query.filter_by(assetId=package.assetId).first()
        package_group = ADI_EST_Show.query.filter_by(assetId=package.assetId).first()
        adi_data.append({
            'Select': f'<input type="radio" name="AssetId" value="{package.assetId}">',
            'Title': package.title,
            'AssetId': package.assetId,
            'Package type': package_main.adi_type,
            'Provider Version': package_main.provider_version,
            'ProviderId': package_main.provider_id,
            'Offer EndDateTime': package_offer.offerEndTime,
            'Parent group id': package_group.parent_group_id,
            'Season number': package_group.season_number,
            'Episode number': package_group.episode_number,
        })

    total = ADI_EST_Show.query.filter(ADI_EST_Show.title.like(search)).count()

    if total == 0:  # If no countries found in the continent
        return errorchecker.no_assets_in_db()
    else:
        json_data = dumps(adi_data, ensure_ascii=False)

    return response.asset_retrieve_form(json_data)


def search_est_assets():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function to Search EST Assets by Title (Non-Case Sensitive) from Database
    :access: public.
    :return: Only EST Single Title, Episodes, Seasons and Box-Sets based on matched title
    """
    title = request.form.get('Title')
    title_uncoded = urllib.parse.unquote_plus(title)
    adi_data = {}
    adi_data['packages'] = []
    search = "%{}%".format(title_uncoded)
    for package in ADI_EST_Show.query.filter(ADI_EST_Show.title.like(search)).\
            order_by(ADI_EST_Show.no_of_seasons.desc()).order_by(ADI_EST_Show.no_of_episodes.desc()).all():
        package_offer = ADI_offer.query.filter_by(assetId=package.assetId).first()
        package_main = ADI_main.query.filter_by(assetId=package.assetId).first()
        package_group = ADI_EST_Show.query.filter_by(assetId=package.assetId).first()
        adi_data['packages'].append({
            'title': package.title,
            'assetId': package.assetId,
            'package type': package_main.adi_type,
            'provider Version': package_main.provider_version,
            'providerId': package_main.provider_id,
            'offer EndDateTime': package_offer.offerEndTime,
            'parent group id': package_group.parent_group_id,
            'season number': package_group.season_number,
            'episode number': package_group.episode_number,
            'ADI': f'<a href="/get_adi/{package.assetId}" class="button_tab">View</a>  '
                   f'<p><a href="/download_adi/{package.assetId}" class="button_tab">Download</a>',
        })

    adi_data['total'] = ADI_EST_Show.query.filter(ADI_EST_Show.title.like(search)).count()

    if adi_data['total'] == 0:  # If no countries found in the continent
        return errorchecker.no_assets_in_db()
    else:
        json_data = dumps(adi_data, ensure_ascii=False)

    return response.asset_retrieve(json_data)


def search_ingest_history(assetId):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function to Search Ingest History on Test Environments based on AssetID
    :access: public.
    :param assetId: Provide Asset ID to search Ingest History
    :return: Ingest history based on the environment
    """
    ingest_data = {}
    ingest_data['history'] = []
    for package in ADI_INGEST_HISTORY.query.filter_by(assetId=assetId).all():
        ingest_data['history'].append({
            'assetId': package.assetId,
            'provider_version': package.provider_version,
            'environment': package.environment,
            'conversationId': package.conversationId,
            'ingest_timestamp': package.ingest_timestamp,
        })

    ingest_data['total'] = ADI_INGEST_HISTORY.query.filter_by(assetId=assetId).count()

    if ingest_data['total'] == 0:  # If no countries found in the continent
        return errorchecker.no_ingest_history(assetId)
    else:
        json_data = dumps(ingest_data)

    return response.asset_retrieve(json_data)


def search_all_files_checksum():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function to return Checksum of all available files in the Supporting Files Directory
    :access: public.
    :return: Checksum of all available files in the Supporting Files Directory
    """
    filedetails = {}
    filedetails['files'] = []
    for file in MEDIA_LIBRARY.query.order_by(MEDIA_LIBRARY.id.desc()).all():
        filedetails['files'].append({
            'filename': file.filename,
            'checksum': file.checksum,
            'image_group': file.image_group,
        })

    filedetails['total'] = MEDIA_LIBRARY.query.count()

    if filedetails['total'] == 0:  # If no countries found in the continent
        return errorchecker.no_files_in_library()
    else:
        json_data = dumps(filedetails)

    return response.asset_retrieve(json_data)

