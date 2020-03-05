# Filename create_asset.py
# This module creates the database entries for different type of assets
from sqlalchemy.orm.session import make_transient
from flask import request
import datetime, time
from .models import ADI_main, ADI_metadata, ADI_offer, ADI_media, ADI_EST_Show, MEDIA_DEFAULT
from . import db, errorchecker, offerdate, response, movie_config, create_purchase_options, create_est_order_type
from .sitemap_create import sitemap_mapper
from .est_show_params import est_show_default_params
from .metadata_params import metadata_default_params
from .image_params import image_default_params

# Call Parameter Functions - These are functions to load default parameter values unless supplied in request
est_params = est_show_default_params()
params = metadata_default_params()  # Checking Default Param Value if Form entry is null
image_set = image_default_params()  # Image classification function
sitemap = sitemap_mapper()  # Jinja template picker


def create_single_title():  # This function creates database entries for all types of Single Titles
    ts = time.time()
    # Getting values from HTML Form
    asset_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')  # Setting current timestamp
    licenseEndTime = offerdate.offer_date(int(request.form.get('LicenseWindow')), 0)  # Adding Window days from now
    offerStartTime = offerdate.offer_date(0, 0)  # Setting Offer Start Time to now
    offerEndTime = offerdate.offer_date(int(request.form.get('offer_window')), 0) # Adding Window days from now
    asset_type = request.form.get('asset_type')
    if (asset_type not in movie_config.default_standard_package) and \
            (asset_type not in movie_config.default_vrp_package):
        return errorchecker.not_supported_asset_type(asset_type)  # Asset type validation
    provider_id = request.form.get('provider_id')
    title = request.form.get('title')
    service_key = request.form.get('service_key')
    params.multiformat_entry(request.form.get('multiformat_id'),asset_timestamp)
    params.param_logic_entry(asset_type)
    params.genre_entry(asset_type)
    params.svod_episode_entry(request.form.get('svod_season_number'), request.form.get('svod_episode_number'),
                              request.form.get('svod_total_episodes'), asset_type, title)  # Only used for Episodes
    params.dpl_entry(request.form.get('dpl_asset_parts'), asset_type, asset_timestamp)
    params.movie_details_entry(provider_id, asset_type)
    params.video_type_entry(provider_id)
    params.offer_type_entry(asset_type)
    params.trailer_entry()
    image_set.image_entry(asset_type)
    path_default = MEDIA_DEFAULT.query.first()

    if (service_key == "") and ('CATCHUP' in asset_type):  # Catchup Missing Input Parameter Check
        return errorchecker.input_missing('service_key')

    try:  # Creating Dictionary for Database Entries
        new_package_main = ADI_main(assetId=asset_timestamp + '01', original_timestamp=asset_timestamp,
                                    adi_type=asset_type, provider_version=params.provider_version,
                                    provider_id=provider_id, multiformat_id=params.multiformat_id)

        new_package_meta = ADI_metadata(assetId=asset_timestamp + '01', title=title, par_rating=params.par_rating,
                                        subtitle_flag=params.subtitle_flag, audio_type=params.audio_type,
                                        frame_rate=params.frame_rate, btc_rating=params.ca_btc,
                                        video_type=params.video_type,synopsis=params.synopsis,
                                        production_year=params.production_year, genre=params.genre,
                                        duration=params.runtime, title_filter='true',
                                        svod_episode_name=params.svod_episode_name,
                                        svod_season_number=params.svod_season_number,
                                        svod_episode_number=params.svod_episode_number,
                                        svod_total_episodes=params.svod_total_episodes,
                                        total_asset_parts=params.dpl_asset_parts, dpl_template=params.dpl_template)

        new_package_offer = ADI_offer(assetId=asset_timestamp + '01', offer_type=params.offer_type,
                                      offerStartTime=offerStartTime, offerEndTime=offerEndTime,
                                      licenseEndTime=licenseEndTime, service_key=service_key, epgTime=offerStartTime)

        new_package_media = ADI_media(assetId=asset_timestamp + '01', video_path=path_default.default_video_path,
                                      image_path=path_default.default_image_path, movie_url=params.movie_url,
                                      movie_checksum=params.movie_checksum, trailer_url=params.trailer_file,
                                      trailer_checksum=params.trailer_checksum, image_url_1=image_set.image_1,
                                      image_checksum_1=image_set.image_1_checksum, image_url_2=image_set.image_2,
                                      image_checksum_2=image_set.image_2_checksum, image_url_3=image_set.image_3,
                                      image_checksum_3=image_set.image_3_checksum, image_url_4=image_set.image_4,
                                      image_checksum_4=image_set.image_4_checksum, image_url_5=image_set.image_5,
                                      image_checksum_5=image_set.image_5_checksum, image_url_6=image_set.image_6,
                                      image_checksum_6=image_set.image_6_checksum)



        db.session.add_all([new_package_main, new_package_meta, new_package_offer, new_package_media])
        db.session.commit()

    except:  # Handling DB error
        return errorchecker.internal_server_error()

    return response.asset_creation_success(asset_timestamp + '01', title)


def create_est_show_adi():  # This function creates database entries for EST Shows (TV and Movie Box-Sets)
    ts = time.time()
    asset_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
    licenseEndTime = offerdate.offer_date(int(request.form.get('LicenseWindow')), 0)
    base_offerStartTime = offerdate.offer_date(0, 0)
    order_type = request.form.get('order_type')
    est_pur_option = request.form.get('po_type')
    show_type = request.form.get('est_show_type')
    title = request.form.get('title')
    est_params.est_show_type_entry(show_type, title)
    est_params.est_series_count((request.form.get('seasons')),(request.form.get('no_of_episodes')))
    show_provider_id = est_params.est_show_provider
    num_of_seasons = int(est_params.no_of_seasons)
    no_of_episodes = int(est_params.no_of_episodes)
    params.param_logic_entry('est_show')
    params.movie_details_entry(show_provider_id, 'est')
    params.offer_type_entry('est_show')
    image_set.image_entry('est_show')
    path_default = MEDIA_DEFAULT.query.first()

    show_new_package_main = ADI_main(assetId=asset_timestamp + '00', original_timestamp=asset_timestamp,
                                    adi_type='est_show', provider_version=params.provider_version,
                                    provider_id=est_params.est_show_provider)

    show_new_package_meta = ADI_metadata(assetId=asset_timestamp + '00', title=title, par_rating=params.par_rating,
                                        btc_rating=params.ca_btc, synopsis=params.synopsis, title_filter='true')

    show_new_package_group = ADI_EST_Show(assetId=asset_timestamp + '00', title=title,
                                          no_of_seasons=str(num_of_seasons), season_number="", no_of_episodes="",
                                          episode_number="", show_type=show_type, parent_group_id="")

    show_new_package_media = ADI_media(assetId=asset_timestamp + '00', image_url_1=image_set.image_1,
                                       video_path=path_default.default_video_path,
                                       image_path=path_default.default_image_path,
                                       image_checksum_1=image_set.image_1_checksum, image_url_2=image_set.image_2,
                                       image_checksum_2=image_set.image_2_checksum, image_url_3=image_set.image_3,
                                       image_checksum_3=image_set.image_3_checksum, image_url_4=image_set.image_4,
                                       image_checksum_4=image_set.image_4_checksum)

    # This section creates database entries for all the Seasons under the Show
    int_timestamp = int(asset_timestamp)
    for season in range(1, num_of_seasons+1):
        season_asset_id = str(int_timestamp + season)
        season_title = title + ':S:' + str(season)
        season_synopsis = season_title + ' Synopsis'
        season_new_package_main = ADI_main(assetId=season_asset_id + '11', original_timestamp=season_asset_id,
                                    adi_type='est_season', provider_version=params.provider_version,
                                    provider_id='est__season_hd')

        season_new_package_meta = ADI_metadata(assetId=season_asset_id + '11', title=season_title,
                                               par_rating=params.par_rating, btc_rating=params.ca_btc,
                                               synopsis=season_synopsis, title_filter='false')

        season_new_package_offer = ADI_offer(assetId=season_asset_id + '11', offer_type=params.offer_type,
                                           offerStartTime=base_offerStartTime, offerEndTime=licenseEndTime,
                                           licenseEndTime=licenseEndTime)

        season_new_package_group = ADI_EST_Show(assetId=season_asset_id + '11', title=season_title,  no_of_seasons="",
                                                season_number=str(season), no_of_episodes=str(no_of_episodes),
                                                episode_number="", show_type=show_type,
                                                parent_group_id=asset_timestamp + '00')

        # This section creates database entries for all the Episodes under the Season
        for episode in range(1, no_of_episodes+1):
            path_default = MEDIA_DEFAULT.query.first()
            episode_asset_id = str(int_timestamp + (season*100) + episode)
            est_params.est_show_type_entry(show_type, season_title)
            episode_title = est_params.est_episode_title + str(episode)
            episode_synopsis = episode_title + ' Synopsis'

            episode_new_package_main = ADI_main(assetId=episode_asset_id + '22', original_timestamp=episode_asset_id,
                                        adi_type='est_episode', provider_version=params.provider_version,
                                        provider_id=est_params.est_episode_provider)

            episode_new_package_meta = ADI_metadata(assetId=episode_asset_id + '22', title=episode_title,
                                                    par_rating=params.par_rating, btc_rating=params.ca_btc,
                                                    synopsis=episode_synopsis, title_filter='false')

            episode_new_package_group = ADI_EST_Show(assetId=episode_asset_id + '22', title=episode_title,
                                                     no_of_seasons="", season_number=str(season), no_of_episodes="",
                                                     episode_number=str(episode), show_type=show_type,
                                                     parent_group_id=season_asset_id + '11')

            episode_new_package_offer = ADI_offer(assetId=episode_asset_id + '22', offer_type=params.offer_type,
                                                 offerStartTime=base_offerStartTime, offerEndTime=licenseEndTime,
                                                 licenseEndTime=licenseEndTime)

            episode_new_package_media = ADI_media(assetId=episode_asset_id + '22',
                                                  video_path=path_default.default_video_path,
                                                  image_path=path_default.default_image_path,
                                                  movie_url=params.movie_url, movie_checksum=params.movie_checksum,
                                                  trailer_url=params.trailer_file,
                                                  trailer_checksum=params.trailer_checksum,
                                                  image_url_1=image_set.image_1,
                                                  image_checksum_1=image_set.image_1_checksum,
                                                  image_url_2=image_set.image_2,
                                                  image_checksum_2=image_set.image_2_checksum,
                                                  image_url_3=image_set.image_3,
                                                  image_checksum_3=image_set.image_3_checksum,
                                                  image_url_4=image_set.image_4,
                                                  image_checksum_4=image_set.image_4_checksum,
                                                  image_url_5=image_set.image_5,
                                                  image_checksum_5=image_set.image_5_checksum,
                                                  image_url_6=image_set.image_6,
                                                  image_checksum_6=image_set.image_6_checksum)

            try:  # Handling DB Transaction Error to add EST Episode. If not added, Seasons and Show not added too
                db.session.add_all([episode_new_package_main, episode_new_package_meta, episode_new_package_meta,
                                    episode_new_package_group, episode_new_package_offer, episode_new_package_media])
                db.session.commit()

                try:  # Handling DB Transaction Error to add EST Season. If not added, Show not added
                    db.session.add_all([season_new_package_main, season_new_package_meta, season_new_package_offer,
                                       season_new_package_group])
                    db.session.commit()

                except:
                    errorchecker.internal_server_error_show('EST_SEASON')
            except:
                errorchecker.internal_server_error_show('EST_EPISODE')

    try:  # Handling DB Transaction Error to add EST Show
        db.session.add_all([show_new_package_main, show_new_package_meta,
                            show_new_package_group, show_new_package_media])
        db.session.commit()

        create_est_order_type.create_est_orders(asset_timestamp, licenseEndTime, order_type, 'est_show')
        create_purchase_options.create_po(est_pur_option, asset_timestamp, 'est_show')
        db.session.commit()

    except:
        errorchecker.internal_server_error_show('EST_SHOW')

    return response.asset_creation_success(asset_timestamp + '00', title)


def create_est_title_adi():  # This function creates database entries for EST Single Titles
    ts = time.time()
    asset_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
    licenseEndTime = offerdate.offer_date(int(request.form.get('LicenseWindow')), 0)
    order_type = request.form.get('order_type')
    est_pur_option = request.form.get('po_type')
    asset_type = 'EST SINGLE TITLE'
    if (asset_type not in movie_config.default_standard_package) and (
            asset_type not in movie_config.default_vrp_package):
        return errorchecker.not_supported_asset_type(asset_type)
    provider_id = movie_config.est_title_provider
    title = request.form.get('title')
    params.param_logic_entry(asset_type)
    params.movie_details_entry(provider_id, asset_type)
    params.video_type_entry(provider_id)
    params.offer_type_entry(asset_type)
    params.trailer_entry()
    image_set.image_entry(asset_type)
    path_default = MEDIA_DEFAULT.query.first()


    new_package_main = ADI_main(assetId=asset_timestamp + '01', original_timestamp=asset_timestamp,
                                adi_type=asset_type, provider_version=params.provider_version, provider_id=provider_id)

    new_package_meta = ADI_metadata(assetId=asset_timestamp + '01', title=title, par_rating=params.par_rating,
                                    subtitle_flag=params.subtitle_flag, audio_type=params.audio_type,
                                    frame_rate=params.frame_rate, btc_rating=params.ca_btc,
                                    video_type=params.video_type, synopsis=params.synopsis,
                                    production_year=params.production_year, duration=params.runtime,
                                    title_filter='true')

    new_package_media = ADI_media(assetId=asset_timestamp + '01', video_path=path_default.default_video_path,
                                  image_path=path_default.default_image_path, movie_url=params.movie_url,
                                  movie_checksum=params.movie_checksum, trailer_url=params.trailer_file,
                                  trailer_checksum=params.trailer_checksum, image_url_1=image_set.image_1,
                                  image_checksum_1=image_set.image_1_checksum, image_url_2=image_set.image_2,
                                  image_checksum_2=image_set.image_2_checksum, image_url_3=image_set.image_3,
                                  image_checksum_3=image_set.image_3_checksum, image_url_4=image_set.image_4,
                                  image_checksum_4=image_set.image_4_checksum, image_url_5=image_set.image_5,
                                  image_checksum_5=image_set.image_5_checksum, image_url_6=image_set.image_6,
                                  image_checksum_6=image_set.image_6_checksum)


    db.session.add_all([new_package_main, new_package_meta, new_package_media])
    create_est_order_type.create_est_orders(asset_timestamp, licenseEndTime, order_type, asset_type)
    create_purchase_options.create_po(est_pur_option, asset_timestamp, asset_type)
    db.session.commit()


    return response.asset_creation_success(asset_timestamp + '01', title)


def clone_asset():
    assetId = request.form.get('AssetId')
    title = request.form.get('title')
    ts = time.time()
    asset_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
    package_main = ADI_main.query.filter_by(assetId=assetId).first()
    if package_main.adi_type == 'EST SINGLE TITLE' or package_main.adi_type == 'est_show':
        return errorchecker.not_supported_asset_type(package_main.adi_type)

    package_media = ADI_media.query.filter_by(assetId=assetId).first()
    package_meta = ADI_metadata.query.filter_by(assetId=assetId).first()
    package_offer = ADI_offer.query.filter_by(assetId=assetId).first()

    db.session.expunge(package_main)
    make_transient(package_main)
    package_main.assetId = asset_timestamp + '01'
    package_main.original_timestamp = asset_timestamp
    package_main.multiformat_id = 'BSKYPR' + asset_timestamp
    package_main.id = None

    db.session.expunge(package_meta)
    make_transient(package_meta)
    package_meta.assetId = asset_timestamp + '01'
    package_meta.title = title
    package_meta.id = None

    db.session.expunge(package_media)
    make_transient(package_media)
    package_media.assetId = asset_timestamp + '01'
    package_media.id = None

    db.session.expunge(package_offer)
    make_transient(package_offer)
    package_offer.assetId = asset_timestamp + '01'
    package_offer.id = None

    db.session.add_all([package_main, package_offer, package_media, package_meta])
    db.session.commit()
    return 'success'







