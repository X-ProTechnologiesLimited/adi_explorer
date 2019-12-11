from flask import Blueprint, render_template, request, jsonify, make_response
import datetime
import time
from . import db
from .models import ADI_main, ADI_metadata, ADI_offer, ADI_media
from . import errorchecker
from . import offerdate
from . import package_logic

def create_single_title():
    ts = time.time()
    asset_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
    LicenseWindow = int(request.form.get('LicenseWindow'))
    licenseEndTime = offerdate.offer_date(LicenseWindow, 0)
    offer_window = int(request.form.get('offer_window'))
    offerStartTime = offerdate.offer_date(0, 0)
    offerEndTime = offerdate.offer_date(offer_window, 0)
    asset_type = request.form.get('asset_type')
    multiformat_id = request.form.get('multiformat_id')
    subtitle_flag = request.form.get('subtitle_flag')
    provider_id = request.form.get('provider_id')
    title = request.form.get('title')
    provider_version = request.form.get('provider_version')
    par_rating_form = request.form.get('par_rating')
    audio_type_form = request.form.get('audio_type')
    frame_rate_form = request.form.get('frame_rate')
    btc_rating_form = request.form.get('ca_btc')
    asset_synopsis = request.form.get('synopsis')
    asset_production_year = request.form.get('production_year')
    asset_mf_id = package_logic.multiformat_entry(multiformat_id, asset_timestamp)
    movie_url = package_logic.movie_file_entry(provider_id)
    movie_checksum = package_logic.movie_checksum_entry(provider_id)
    video_type = package_logic.video_type_entry(provider_id)
    offer_type = package_logic.offer_type_entry(asset_type)
    synopsis = package_logic.synopsis_entry(asset_synopsis, title)
    production_year = package_logic.production_year_entry(asset_production_year)
    par_rating = package_logic.par_rating_entry(par_rating_form)
    audio_type = package_logic.audio_type_entry(audio_type_form)
    frame_rate = package_logic.frame_rate_entry(frame_rate_form)
    btc_rating = package_logic.btc_entry(btc_rating_form)

    sitemap = package_logic.sitemap_entry(asset_type, subtitle_flag)
    if sitemap == False:
        return errorchecker.not_supported_asset_type(asset_type)

    try:
        new_package_main = ADI_main(assetId=asset_timestamp + '01', original_timestamp=asset_timestamp,
                                    adi_type=asset_type, provider_version=provider_version,
                                    provider_id=provider_id, multiformat_id=asset_mf_id)

        new_package_meta = ADI_metadata(assetId=asset_timestamp + '01', title=title, par_rating=par_rating,
                                        subtitle_flag=subtitle_flag, audio_type=audio_type,
                                        frame_rate=frame_rate, btc_rating=btc_rating, video_type=video_type,
                                        synopsis=synopsis, production_year=production_year)

        new_package_offer = ADI_offer(assetId=asset_timestamp + '01', offer_type=offer_type,
                                      offerStartTime=offerStartTime, offerEndTime=offerEndTime,
                                      licenseEndTime=licenseEndTime)

        new_package_media = ADI_media(assetId=asset_timestamp + '01', movie_url=movie_url,
                                      movie_checksum=movie_checksum)

        db.session.add(new_package_main)
        db.session.add(new_package_meta)
        db.session.add(new_package_offer)
        db.session.add(new_package_media)
        db.session.commit()

    except:
        return errorchecker.internal_server_error()

    return package_logic.download_adi_package(asset_timestamp + '01')