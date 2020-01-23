from flask import request
import datetime
import time
from . import db
from .models import ADI_main, ADI_metadata, ADI_offer, ADI_media, ADI_EST_Show
from . import errorchecker
from . import offerdate
from .sitemap_create import sitemap_mapper
from . import response
from .est_show_params import est_show_default_params
from .metadata_params import metadata_default_params
est_params = est_show_default_params()
params = metadata_default_params()
sitemap = sitemap_mapper()

def create_single_title():
    ts = time.time()
    asset_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
    licenseEndTime = offerdate.offer_date(int(request.form.get('LicenseWindow')), 0)
    offerStartTime = offerdate.offer_date(0, 0)
    offerEndTime = offerdate.offer_date(int(request.form.get('offer_window')), 0)
    asset_type = request.form.get('asset_type')
    provider_id = request.form.get('provider_id')
    title = request.form.get('title')
    service_key = request.form.get('service_key')
    params.multiformat_entry(request.form.get('multiformat_id'),asset_timestamp)
    params.param_logic_entry(request.form.get('synopsis'), request.form.get('title'),
                             request.form.get('provider_version'),
                             request.form.get('production_year'), request.form.get('ca_btc'),
                             request.form.get('par_rating'),
                             request.form.get('audio_type'), request.form.get('frame_rate'),
                             request.form.get('subtitle_flag'), request.form.get('duration'),
                             request.form.get('svod_season_number'), request.form.get('svod_episode_number'),
                             request.form.get('svod_total_episodes'))
    svod_episode_name = 'EpisodeName for: ' + title + ', Season: ' + params.svod_season_number + ', Episode: ' + \
                        params.svod_episode_number
    params.movie_details_entry(provider_id)
    params.video_type_entry(provider_id)
    params.offer_type_entry(asset_type)
    sitemap.sitemap_entry(asset_type,params.subtitle_flag)
    if sitemap.sitemap == False:
        return errorchecker.not_supported_asset_type(asset_type)

    if (service_key == "") and ('CATCHUP' in asset_type):
        return errorchecker.input_missing('service_key')

    try:
        new_package_main = ADI_main(assetId=asset_timestamp + '01', original_timestamp=asset_timestamp,
                                    adi_type=asset_type, provider_version=params.provider_version,
                                    provider_id=provider_id, multiformat_id=params.multiformat_id)

        new_package_meta = ADI_metadata(assetId=asset_timestamp + '01', title=title, par_rating=params.par_rating,
                                        subtitle_flag=params.subtitle_flag, audio_type=params.audio_type,
                                        frame_rate=params.frame_rate, btc_rating=params.ca_btc, video_type=params.video_type,
                                        synopsis=params.synopsis, production_year=params.production_year,
                                        duration=params.runtime, title_filter='true', svod_episode_name=svod_episode_name,
                                        svod_season_number=params.svod_season_number,
                                        svod_episode_number=params.svod_episode_number,
                                        svod_total_episodes=params.svod_total_episodes)

        new_package_offer = ADI_offer(assetId=asset_timestamp + '01', offer_type=params.offer_type,
                                      offerStartTime=offerStartTime, offerEndTime=offerEndTime,
                                      licenseEndTime=licenseEndTime, service_key=service_key, epgTime=offerStartTime)

        new_package_media = ADI_media(assetId=asset_timestamp + '01', movie_url=params.movie_url,
                                      movie_checksum=params.movie_checksum)

        db.session.add(new_package_main)
        db.session.add(new_package_meta)
        db.session.add(new_package_offer)
        db.session.add(new_package_media)
        db.session.commit()

    except:
        return errorchecker.internal_server_error()

    return response.asset_creation_success(asset_timestamp + '01', title)


def create_est_show_adi():
    ts = time.time()
    asset_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
    licenseEndTime = offerdate.offer_date(int(request.form.get('LicenseWindow')), 0)
    offerStartTime = offerdate.offer_date(0, 0)
    offerEndTime = offerdate.offer_date(int(request.form.get('offer_window')), 0)
    show_type = request.form.get('est_show_type')
    title = request.form.get('title')
    est_params.est_show_type_entry(show_type, title)
    est_params.est_series_count((request.form.get('seasons')),(request.form.get('no_of_episodes')))
    show_provider_id = est_params.est_show_provider
    num_of_seasons = int(est_params.no_of_seasons)
    no_of_episodes = int(est_params.no_of_episodes)
    params.param_logic_entry(request.form.get('synopsis'), request.form.get('title'),
                             request.form.get('provider_version'),
                             request.form.get('production_year'), request.form.get('ca_btc'),
                             request.form.get('par_rating'),
                             request.form.get('audio_type'), request.form.get('frame_rate'),
                             request.form.get('subtitle_flag'), "")
    params.movie_details_entry(show_provider_id)
    params.offer_type_entry('est_show')

    show_new_package_main = ADI_main(assetId=asset_timestamp + '00', original_timestamp=asset_timestamp,
                                    adi_type='est_show', provider_version=params.provider_version,
                                    provider_id=est_params.est_show_provider)

    show_new_package_meta = ADI_metadata(assetId=asset_timestamp + '00', title=title, par_rating=params.par_rating,
                                        btc_rating=params.ca_btc, synopsis=params.synopsis, title_filter='true')

    show_new_package_offer = ADI_offer(assetId=asset_timestamp + '00', offer_type=params.offer_type,
                                      offerStartTime=offerStartTime, offerEndTime=offerEndTime,
                                      licenseEndTime=licenseEndTime)

    show_new_package_group = ADI_EST_Show(assetId=asset_timestamp + '00', title=title, no_of_seasons=str(num_of_seasons),
                                         season_number="", no_of_episodes="", episode_number="",
                                          show_type=show_type, parent_group_id="")


    int_timestamp = int(asset_timestamp)
    for season in range(1, num_of_seasons+1):
        season_asset_id = str(int_timestamp + season)
        season_title = title + ': Season_' + str(season)
        season_synopsis = season_title + ' Synopsis'
        season_new_package_main = ADI_main(assetId=season_asset_id + '11', original_timestamp=season_asset_id,
                                    adi_type='est_season', provider_version=params.provider_version,
                                    provider_id='est__season_hd')

        season_new_package_meta = ADI_metadata(assetId=season_asset_id + '11', title=season_title, par_rating=params.par_rating,
                                        btc_rating=params.ca_btc, synopsis=season_synopsis, title_filter='false')

        season_new_package_offer = ADI_offer(assetId=season_asset_id + '11', offer_type=params.offer_type,
                                           offerStartTime=offerStartTime, offerEndTime=offerEndTime,
                                           licenseEndTime=licenseEndTime)

        season_new_package_group = ADI_EST_Show(assetId=season_asset_id + '11', title=season_title,  no_of_seasons="",
                                                season_number=str(season), no_of_episodes=str(no_of_episodes),
                                                episode_number="", show_type=show_type, parent_group_id=asset_timestamp + '00')

        for episode in range(1, no_of_episodes+1):
            episode_asset_id = str(int_timestamp + (season*100) + episode)
            est_params.est_show_type_entry(show_type, season_title)
            episode_title = est_params.est_episode_title + str(episode)
            episode_synopsis = episode_title + ' Synopsis'

            episode_new_package_main = ADI_main(assetId=episode_asset_id + '22', original_timestamp=episode_asset_id,
                                        adi_type='est_episode', provider_version=params.provider_version,
                                        provider_id=est_params.est_episode_provider)

            episode_new_package_meta = ADI_metadata(assetId=episode_asset_id + '22', title=episode_title, par_rating=params.par_rating,
                                            btc_rating=params.ca_btc, synopsis=episode_synopsis, title_filter='false')

            episode_new_package_group = ADI_EST_Show(assetId=episode_asset_id + '22', title=episode_title, no_of_seasons="",
                                                     season_number=str(season), no_of_episodes="", episode_number=str(episode),
                                                     show_type=show_type, parent_group_id=season_asset_id + '11')

            episode_new_package_offer = ADI_offer(assetId=episode_asset_id + '22', offer_type=params.offer_type,
                                                 offerStartTime=offerStartTime, offerEndTime=offerEndTime,
                                                 licenseEndTime=licenseEndTime)

            episode_new_package_media = ADI_media(assetId=episode_asset_id + '22', movie_url=params.movie_url,
                                                  movie_checksum=params.movie_checksum)

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

    return response.asset_creation_success(asset_timestamp + '00', title)



