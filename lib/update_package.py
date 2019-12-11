from flask import Blueprint, render_template, request
from . import db
from .models import ADI_main, ADI_metadata, ADI_offer, ADI_media
from . import errorchecker
from . import response

def update_single_title():
    assetId = request.form.get('AssetId')
    update_field = request.form.get('asset_field')
    field_value = request.form.get('value')
    try:
        package = ADI_main.query.filter_by(assetId=assetId).first()
        if update_field == 'title':
            package = ADI_metadata.query.filter_by(assetId=assetId).update(dict(title=field_value))
        elif update_field == 'offerStartTime':
            package = ADI_offer.query.filter_by(assetId=assetId).update(dict(offerStartTime=field_value))
        elif update_field == 'offerEndTime':
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


def update_asset_video():
    assetId = request.form.get('AssetId')
    movie_url = request.form.get('movie_url')
    movie_checksum = request.form.get('movie_checksum')
    try:
        package = ADI_main.query.filter_by(assetId=assetId).first()
        provider_version = int(package.provider_version)
        updated_provider_version = (provider_version + 1)
        package = ADI_media.query.filter_by(assetId=assetId).update(dict(movie_url=movie_url, movie_checksum=movie_checksum))
        package = ADI_main.query.filter_by(assetId=assetId).update(dict(provider_version=str(updated_provider_version)))
        db.session.commit()
        return response.asset_update_success(assetId, 'movie')
    except:
        return errorchecker.asset_not_found_id(assetId)