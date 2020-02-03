from flask import request
from . import db
from .models import ADI_main, ADI_metadata, ADI_offer, ADI_media, MEDIA_DEFAULT, MEDIA_LIBRARY
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
        elif update_field == 'synopsis':
            package = ADI_metadata.query.filter_by(assetId=assetId).update(dict(synopsis=field_value))
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
        elif update_field == 'duration':
            package = ADI_metadata.query.filter_by(assetId=assetId).update(dict(duration=field_value))
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


def update_default_fields():
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

