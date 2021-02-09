# Filename: lib/update_package.py
"""
Created on June 01, 2020

@author: Krishnendu Banerjee
@summary: This file holds the functions to perform different metadata updates on assets in Database
"""
from flask import request
from . import db, errorchecker, response
from .models import ADI_main, ADI_metadata, ADI_offer, ADI_media, MEDIA_DEFAULT, MEDIA_LIBRARY

def update_single_title():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function for updating metadata for Assets
    :access: public
    :form_input : assetId
    :form_input : update_field (Parameter that will be updated)
    :return: Success or Failure and commit DB with metadata updates for AssetId
    """
    assetId = request.form.get('AssetId')
    update_field = request.form.get('asset_field')
    offerId = request.form.get('offerId')
    field_value = request.form.get('value')

    try:
        package = ADI_main.query.filter_by(assetId=assetId).first()
        if update_field == 'title':
            package = ADI_metadata.query.filter_by(assetId=assetId).update(dict(title=field_value))
        elif update_field == 'synopsis':
            package = ADI_metadata.query.filter_by(assetId=assetId).update(dict(synopsis=field_value))
        elif update_field == 'offerStartTime':
            if package.adi_type == 'EST SINGLE TITLE' or package.adi_type == 'est_show':
                package = ADI_offer.query.filter_by(est_offerId=offerId).update(dict(offerStartTime=field_value))
            else:
                package = ADI_offer.query.filter_by(assetId=assetId).update(dict(offerStartTime=field_value))
        elif update_field == 'offerEndTime':
            if package.adi_type == 'EST SINGLE TITLE' or package.adi_type == 'est_show':
                package = ADI_offer.query.filter_by(est_offerId=offerId).update(dict(offerEndTime=field_value))
            else:
                package = ADI_offer.query.filter_by(assetId=assetId).update(dict(offerEndTime=field_value))
        elif update_field == 'licenseEndTime':
            package = ADI_offer.query.filter_by(assetId=assetId).update(dict(licenseEndTime=field_value))
        elif update_field == 'audio_type':
            package = ADI_metadata.query.filter_by(assetId=assetId).update(dict(audio_type=field_value))
        elif update_field == 'frame_rate':
            package = ADI_metadata.query.filter_by(assetId=assetId).update(dict(frame_rate=field_value))
        elif update_field == 'par_rating':
            package = ADI_metadata.query.filter_by(assetId=assetId).update(dict(par_rating=field_value))
        elif update_field == 'btc_rating':
            package = ADI_metadata.query.filter_by(assetId=assetId).update(dict(btc_rating=field_value))
        elif update_field == 'subtitle_flag':
            package = ADI_metadata.query.filter_by(assetId=assetId).update(dict(subtitle_flag=field_value))
        elif update_field == 'multiformat_id':
            package = ADI_main.query.filter_by(assetId=assetId).update(dict(multiformat_id=field_value))
        elif update_field == 'subtitle_lang':
            package = ADI_metadata.query.filter_by(assetId=assetId).update(dict(subtitle_lang=field_value))
        elif update_field == 'duration':
            package = ADI_metadata.query.filter_by(assetId=assetId).update(dict(duration=field_value))
        elif update_field == 'genre':
            package = ADI_metadata.query.filter_by(assetId=assetId).update(dict(genre=field_value))
        elif update_field == 'provider_id':
            package = ADI_main.query.filter_by(assetId=assetId).update(dict(provider_id=field_value))
        elif update_field == 'delete_verb':
            package = ADI_main.query.filter_by(assetId=assetId).update(dict(is_deleted=field_value))
        elif update_field == 'content_marker':
            package = ADI_main.query.filter_by(assetId=assetId).update(dict(content_marker=field_value,
                                                                            cm_media_id=request.form.get('cm_media_id'),
                                                                            cm_type=request.form.get('cm_media_type'),
                                                                            cm_value=request.form.get('cm_media_value')))
        else:
            return errorchecker.undefined_update_field(update_field)

        db.session.commit()
        package_updated = ADI_main.query.filter_by(assetId=assetId).first()
        provider_version = int(package_updated.provider_version)
        updated_provider_version = (provider_version + 1)
        package = ADI_main.query.filter_by(assetId=assetId).update(dict(provider_version=str(updated_provider_version)))
        db.session.commit()
        return response.asset_update_success(assetId, update_field)
    except:
        return errorchecker.asset_not_found_id(assetId)


def update_asset_video(movie_type):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function to update Movie or Trailer for an asset
    :access: public
    :form_input : assetId
    :form_input : video_filename
    :form_input : video_checksum
    :param movie_type: movie/trailer
    :return: Success or Failure for the Movie/Trailer update
    """
    assetId = request.form.get('AssetId')
    filename = request.form.get('video_filename')
    checksum = request.form.get('video_checksum')
    try:
        package = ADI_main.query.filter_by(assetId=assetId).first()
        provider_version = int(package.provider_version)
        updated_provider_version = (provider_version + 1)
        if movie_type == 'movie':
            package = ADI_media.query.filter_by(assetId=assetId).update(
                dict(movie_url=filename, movie_checksum=checksum))
        else:
            package = ADI_media.query.filter_by(assetId=assetId).update(
                dict(trailer_url=filename, trailer_checksum=checksum))

        package = ADI_main.query.filter_by(assetId=assetId).update(dict(provider_version=str(updated_provider_version)))
        db.session.commit()
        return response.asset_update_success(assetId, movie_type)
    except:
        return errorchecker.asset_not_found_id(assetId)


def update_default_fields():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function to update Default Media Parameters
    :access: public
    :form_input : config_name
    :form_input : value
    :form_input : checksum
    :return: Success or Failure for the default_field_update
    """
    update_field = request.form.get('config_name')
    field_value = request.form.get('value')
    video_checksum = request.form.get('checksum')
    if update_field == 'Image Path':
        default_config = MEDIA_DEFAULT.query.update(dict(default_image_path=field_value))
    elif update_field == 'Video Path':
        default_config = MEDIA_DEFAULT.query.update(dict(default_video_path=field_value))
    elif update_field == 'Standard Image Prefix':
        default_config = MEDIA_DEFAULT.query.update(dict(standard_image_file_prefix=field_value))
    elif update_field == 'DPL Image Prefix':
        default_config = MEDIA_DEFAULT.query.update(dict(dpl_image_file_prefix=field_value))
    elif update_field == 'HD Video File':
        default_config = MEDIA_DEFAULT.query.update(dict(hd_movie_file=field_value))
        media = MEDIA_LIBRARY.query.filter_by(filename=field_value).first()
        if not media:
            new_media = MEDIA_LIBRARY(filename=field_value, checksum=video_checksum)
            db.session.add(new_media)
    elif update_field == 'SD Video File':
        default_config = MEDIA_DEFAULT.query.update(dict(title_movie_file=field_value))
        media = MEDIA_LIBRARY.query.filter_by(filename=field_value).first()
        if not media:
            new_media = MEDIA_LIBRARY(filename=field_value, checksum=video_checksum)
            db.session.add(new_media)
    elif update_field == '4k Video File':
        default_config = MEDIA_DEFAULT.query.update(dict(sdr_movie_file=field_value))
        media = MEDIA_LIBRARY.query.filter_by(filename=field_value).first()
        if not media:
            new_media = MEDIA_LIBRARY(filename=field_value, checksum=video_checksum)
            db.session.add(new_media)
    elif update_field == 'HDR Video File':
        default_config = MEDIA_DEFAULT.query.update(dict(hdr_movie_file=field_value))
        media = MEDIA_LIBRARY.query.filter_by(filename=field_value).first()
        if not media:
            new_media = MEDIA_LIBRARY(filename=field_value, checksum=video_checksum)
            db.session.add(new_media)
    elif update_field == 'EST Video File':
        default_config = MEDIA_DEFAULT.query.update(dict(est_movie_file=field_value))
        media = MEDIA_LIBRARY.query.filter_by(filename=field_value).first()
        if not media:
            new_media = MEDIA_LIBRARY(filename=field_value, checksum=video_checksum)
            db.session.add(new_media)
    elif update_field == 'DPL Video File':
        default_config = MEDIA_DEFAULT.query.update(dict(dpl_movie_file=field_value))
        media = MEDIA_LIBRARY.query.filter_by(filename=field_value).first()
        if not media:
            new_media = MEDIA_LIBRARY(filename=field_value, checksum=video_checksum)
            db.session.add(new_media)
    elif update_field == 'Trailer Video File':
        default_config = MEDIA_DEFAULT.query.update(dict(trailer=field_value))
        media = MEDIA_LIBRARY.query.filter_by(filename=field_value).first()
        if not media:
            new_media = MEDIA_LIBRARY(filename=field_value, checksum=video_checksum)
            db.session.add(new_media)
    else:
        return errorchecker.undefined_update_field(update_field)

    try:
        db.session.commit()
        return response.default_config_load_success(update_field, field_value)
    except:
        return errorchecker.internal_server_error()


