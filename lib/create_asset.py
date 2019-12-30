from flask import Blueprint, render_template, request, jsonify, make_response
import datetime
import time
from . import db
from .models import ADI_main, ADI_metadata, ADI_offer, ADI_media, ADI_EST_Show
from . import errorchecker
from . import offerdate
from . import package_logic
from . import get_asset_details

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
    sub_flag = request.form.get('subtitle_flag')
    provider_id = request.form.get('provider_id')
    title = request.form.get('title')
    provider_version = request.form.get('provider_version')
    par_rating_form = request.form.get('par_rating')
    audio_type_form = request.form.get('audio_type')
    frame_rate_form = request.form.get('frame_rate')
    btc_rating_form = request.form.get('ca_btc')
    asset_synopsis = request.form.get('synopsis')
    asset_production_year = request.form.get('production_year')
    service_key = request.form.get('service_key')
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
    subtitle_flag = package_logic.subtitle_entry(sub_flag)

    sitemap = package_logic.sitemap_entry(asset_type, subtitle_flag)
    if sitemap == False:
        return errorchecker.not_supported_asset_type(asset_type)

    if (service_key == "") and (asset_type == 'CATCHUP'):
        return errorchecker.input_missing('service_key')

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
                                      licenseEndTime=licenseEndTime, service_key=service_key, epgTime=offerStartTime)

        new_package_media = ADI_media(assetId=asset_timestamp + '01', movie_url=movie_url,
                                      movie_checksum=movie_checksum)

        db.session.add(new_package_main)
        db.session.add(new_package_meta)
        db.session.add(new_package_offer)
        db.session.add(new_package_media)
        db.session.commit()

    except:
        return errorchecker.internal_server_error()

    return get_asset_details.download_adi_package(asset_timestamp + '01')


def create_est_show_adi():
    ts = time.time()
    asset_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
    LicenseWindow = int(request.form.get('LicenseWindow'))
    licenseEndTime = offerdate.offer_date(LicenseWindow, 0)
    offer_window = int(request.form.get('offer_window'))
    offerStartTime = offerdate.offer_date(0, 0)
    offerEndTime = offerdate.offer_date(offer_window, 0)
    show_type = request.form.get('est_show_type')
    no_of_episodes = int(request.form.get('no_of_episodes'))
    num_of_seasons = int(request.form.get('seasons'))
    asset_type = 'est_show'
    show_provider_id = package_logic.est_show_provider(show_type)
    episode_provider_id = package_logic.est_episode_provider(show_type)
    season_provider_id = 'est__season_hd'
    title = request.form.get('title')
    provider_version = '1'
    par_rating_form = request.form.get('par_rating')
    btc_rating_form = request.form.get('ca_btc')
    asset_synopsis = request.form.get('synopsis')
    movie_url = package_logic.movie_file_entry(show_provider_id)
    movie_checksum = package_logic.movie_checksum_entry(show_provider_id)
    offer_type = package_logic.offer_type_entry(asset_type)
    synopsis = package_logic.synopsis_entry(asset_synopsis, title)
    par_rating = package_logic.par_rating_entry(par_rating_form)
    btc_rating = package_logic.btc_entry(btc_rating_form)


    show_new_package_main = ADI_main(assetId=asset_timestamp + '00', original_timestamp=asset_timestamp,
                                    adi_type=asset_type, provider_version=provider_version,
                                    provider_id=show_provider_id)

    show_new_package_meta = ADI_metadata(assetId=asset_timestamp + '00', title=title, par_rating=par_rating,
                                        btc_rating=btc_rating, synopsis=synopsis)

    show_new_package_offer = ADI_offer(assetId=asset_timestamp + '00', offer_type=offer_type,
                                      offerStartTime=offerStartTime, offerEndTime=offerEndTime,
                                      licenseEndTime=licenseEndTime)

    show_new_package_group = ADI_EST_Show(assetId=asset_timestamp + '00', no_of_seasons=str(num_of_seasons),
                                         no_of_episodes=str(no_of_episodes), show_type=show_type)


    int_timestamp = int(asset_timestamp)
    for season in range(1, num_of_seasons+1):
        season_asset_id = str(int_timestamp + season)
        season_title = title + ': Season_' + str(season)
        season_synopsis = season_title + ' Synopsis'
        season_new_package_main = ADI_main(assetId=season_asset_id + str(season) + '1', original_timestamp=season_asset_id,
                                    adi_type='est_season', provider_version=provider_version,
                                    provider_id=season_provider_id)

        season_new_package_meta = ADI_metadata(assetId=season_asset_id + str(season) + '1', title=season_title, par_rating=par_rating,
                                        btc_rating=btc_rating, synopsis=season_synopsis)

        season_new_package_offer = ADI_offer(assetId=season_asset_id + str(season) + '1', offer_type=offer_type,
                                           offerStartTime=offerStartTime, offerEndTime=offerEndTime,
                                           licenseEndTime=licenseEndTime)

        season_new_package_group = ADI_EST_Show(assetId=season_asset_id + str(season) + '1', season_number=str(season),
                                         no_of_episodes=str(no_of_episodes), show_type=show_type,
                                         parent_group_id=asset_timestamp + '00')

        for episode in range(1, no_of_episodes+1):
            episode_asset_id = str(int_timestamp + (season*100) + episode)
            episode_title = season_title + ': Episode: ' + str(episode)
            episode_synopsis = episode_title + ' Synopsis'

            episode_new_package_main = ADI_main(assetId=episode_asset_id + '22', original_timestamp=episode_asset_id,
                                        adi_type='est_episode', provider_version=provider_version,
                                        provider_id=episode_provider_id)

            episode_new_package_meta = ADI_metadata(assetId=episode_asset_id + '22', title=episode_title, par_rating=par_rating,
                                            btc_rating=btc_rating, synopsis=episode_synopsis)

            episode_new_package_group = ADI_EST_Show(assetId=episode_asset_id + '22', season_number=str(season),
                                             episode_number=str(episode), show_type=show_type,
                                             parent_group_id=season_asset_id + '11')

            episode_new_package_offer = ADI_offer(assetId=episode_asset_id + '22', offer_type=offer_type,
                                                 offerStartTime=offerStartTime, offerEndTime=offerEndTime,
                                                 licenseEndTime=licenseEndTime)

            episode_new_package_media = ADI_media(assetId=episode_asset_id + '22', movie_url=movie_url,
                                                  movie_checksum=movie_checksum)

            try:
                db.session.add(episode_new_package_main)
                db.session.add(episode_new_package_meta)
                db.session.add(episode_new_package_group)
                db.session.add(episode_new_package_offer)
                db.session.add(episode_new_package_media)
                db.session.commit()

                try:
                    db.session.add(season_new_package_main)
                    db.session.add(season_new_package_meta)
                    db.session.add(season_new_package_offer)
                    db.session.add(season_new_package_group)
                    db.session.commit()

                    try:
                        db.session.add(show_new_package_main)
                        db.session.add(show_new_package_meta)
                        db.session.add(show_new_package_offer)
                        db.session.add(show_new_package_group)
                        db.session.commit()

                    except:
                        errorchecker.internal_server_error_show('EST_SHOW')
                except:
                    errorchecker.internal_server_error_show('EST-SEASON')
            except:
                errorchecker.internal_server_error_show('EST_EPISODE')

    return 'Successfully Created EST Show'



