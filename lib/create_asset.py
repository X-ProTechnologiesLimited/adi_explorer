# Filename create_asset.py
from flask import request
import datetime, time
from .models import ADI_main, ADI_metadata, ADI_offer, ADI_media, ADI_EST_Show, MEDIA_DEFAULT, EST_PO
from . import db, errorchecker, offerdate, response, movie_config, create_purchase_options
from .sitemap_create import sitemap_mapper
from .est_show_params import est_show_default_params
from .metadata_params import metadata_default_params
from .image_params import image_default_params

# Call Parameter Functions
est_params = est_show_default_params()
params = metadata_default_params()
image_set = image_default_params()
sitemap = sitemap_mapper()


def create_single_title():
    # This function creates database entries for all types of Single Titles
    ts = time.time()
    asset_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
    licenseEndTime = offerdate.offer_date(int(request.form.get('LicenseWindow')), 0)
    offerStartTime = offerdate.offer_date(0, 0)
    offerEndTime = offerdate.offer_date(int(request.form.get('offer_window')), 0)
    asset_type = request.form.get('asset_type')
    if (asset_type not in movie_config.default_standard_package) and (asset_type not in movie_config.default_vrp_package):
        return errorchecker.not_supported_asset_type(asset_type) # Asset type check
    provider_id = request.form.get('provider_id')
    title = request.form.get('title')
    service_key = request.form.get('service_key')
    params.multiformat_entry(request.form.get('multiformat_id'),asset_timestamp)
    params.param_logic_entry(asset_type)
    params.genre_entry(asset_type)
    params.svod_episode_entry(request.form.get('svod_season_number'), request.form.get('svod_episode_number'),
                              request.form.get('svod_total_episodes'), asset_type, title) # Only used for Episode Types
    params.dpl_entry(request.form.get('dpl_asset_parts'), asset_type, asset_timestamp)
    params.movie_details_entry(provider_id, asset_type)
    params.video_type_entry(provider_id)
    params.offer_type_entry(asset_type)
    params.trailer_entry()
    image_set.image_entry(asset_type)
    path_default = MEDIA_DEFAULT.query.first()

    if (service_key == "") and ('CATCHUP' in asset_type):
        return errorchecker.input_missing('service_key')

    try:
        new_package_main = ADI_main(assetId=asset_timestamp + '01', original_timestamp=asset_timestamp,
                                    adi_type=asset_type, provider_version=params.provider_version,
                                    provider_id=provider_id, multiformat_id=params.multiformat_id)

        new_package_meta = ADI_metadata(assetId=asset_timestamp + '01', title=title, par_rating=params.par_rating,
                                        subtitle_flag=params.subtitle_flag, audio_type=params.audio_type,
                                        frame_rate=params.frame_rate, btc_rating=params.ca_btc, video_type=params.video_type,
                                        synopsis=params.synopsis, production_year=params.production_year, genre=params.genre,
                                        duration=params.runtime, title_filter='true', svod_episode_name=params.svod_episode_name,
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

    show_new_package_offer = ADI_offer(assetId=asset_timestamp + '00', offer_type=params.offer_type,
                                      offerStartTime=offerStartTime, offerEndTime=offerEndTime,
                                      licenseEndTime=licenseEndTime)

    show_new_package_group = ADI_EST_Show(assetId=asset_timestamp + '00', title=title, no_of_seasons=str(num_of_seasons),
                                         season_number="", no_of_episodes="", episode_number="",
                                          show_type=show_type, parent_group_id="")

    show_new_package_media = ADI_media(assetId=asset_timestamp + '00', image_url_1=image_set.image_1,
                                       video_path=path_default.default_video_path,
                                       image_path=path_default.default_image_path,
                                       image_checksum_1=image_set.image_1_checksum, image_url_2=image_set.image_2,
                                       image_checksum_2=image_set.image_2_checksum, image_url_3=image_set.image_3,
                                       image_checksum_3=image_set.image_3_checksum, image_url_4=image_set.image_4,
                                       image_checksum_4=image_set.image_4_checksum)


    int_timestamp = int(asset_timestamp)
    for season in range(1, num_of_seasons+1):
        season_asset_id = str(int_timestamp + season)
        season_title = title + ':S:' + str(season)
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
            path_default = MEDIA_DEFAULT.query.first()
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

            episode_new_package_media = ADI_media(assetId=episode_asset_id + '22',
                                                  video_path=path_default.default_video_path,
                                                  image_path=path_default.default_image_path,
                                                  movie_url=params.movie_url, movie_checksum=params.movie_checksum,
                                                  trailer_url=params.trailer_file, trailer_checksum=params.trailer_checksum,
                                                  image_url_1=image_set.image_1, image_checksum_1=image_set.image_1_checksum,
                                                  image_url_2=image_set.image_2, image_checksum_2=image_set.image_2_checksum,
                                                  image_url_3=image_set.image_3, image_checksum_3=image_set.image_3_checksum,
                                                  image_url_4=image_set.image_4, image_checksum_4=image_set.image_4_checksum,
                                                  image_url_5=image_set.image_5, image_checksum_5=image_set.image_5_checksum,
                                                  image_url_6=image_set.image_6, image_checksum_6=image_set.image_6_checksum)

            try:
                db.session.add_all([episode_new_package_main, episode_new_package_meta, episode_new_package_meta,
                                    episode_new_package_group, episode_new_package_offer, episode_new_package_media])
                db.session.commit()

                try:
                    db.session.add_all([season_new_package_main, season_new_package_meta, season_new_package_offer,
                                       season_new_package_group])
                    db.session.commit()

                    try:
                        db.session.add_all([show_new_package_main, show_new_package_meta, show_new_package_offer,
                                        show_new_package_group, show_new_package_media])
                        db.session.commit()

                    except:
                        errorchecker.internal_server_error_show('EST_SHOW')
                except:
                    errorchecker.internal_server_error_show('EST_SEASON')
            except:
                errorchecker.internal_server_error_show('EST_EPISODE')

    return response.asset_creation_success(asset_timestamp + '00', title)


def create_est_title_adi():
    ts = time.time()
    asset_timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
    licenseEndTime = offerdate.offer_date(int(request.form.get('LicenseWindow')), 0)
    order_type = request.form.get('order_type')
    est_pur_option = request.form.get('po_type')
    est_params.est_offer_window_entry(request.form.get('po_offer_window'), request.form.get('cs_offer_window'),
                                      request.form.get('reg_offer_window'))
    est_params.est_offer_date_entry(order_type, est_params.po_offer_window, est_params.cs_offer_window,
                                    est_params.reg_offer_window)
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
                                    frame_rate=params.frame_rate, btc_rating=params.ca_btc, video_type=params.video_type,
                                    synopsis=params.synopsis, production_year=params.production_year,
                                    duration=params.runtime, title_filter='true')

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


    if order_type == "PO":
        new_package_offer_PO = ADI_offer(assetId=asset_timestamp + '01', offer_type=params.offer_type,
                                         offerStartTime=est_params.po_start, offerEndTime=est_params.po_end,
                                         licenseEndTime=licenseEndTime, est_order_type='PreOrder',
                                         est_offerId=asset_timestamp + '01')

        db.session.add(new_package_offer_PO)
    elif order_type == "REG":
        new_package_offer_REG = ADI_offer(assetId=asset_timestamp + '01', offer_type=params.offer_type,
                                         offerStartTime=est_params.reg_start, offerEndTime=est_params.reg_end,
                                         licenseEndTime=licenseEndTime, est_order_type='Regular',
                                         est_offerId=asset_timestamp + '01')

        db.session.add(new_package_offer_REG)

    elif order_type == "PO+CS":
        new_package_offer_CS = ADI_offer(assetId=asset_timestamp + '01', offer_type=params.offer_type,
                                         offerStartTime=est_params.cs_start, offerEndTime=est_params.cs_end,
                                         licenseEndTime=licenseEndTime, est_order_type='ComingSoon',
                                         est_offerId=asset_timestamp + '01')

        new_package_offer_PO = ADI_offer(assetId=asset_timestamp + '01', offer_type=params.offer_type,
                                         offerStartTime=est_params.po_start, offerEndTime=est_params.po_end,
                                         licenseEndTime=licenseEndTime, est_order_type='PreOrder',
                                         est_offerId=asset_timestamp + '02')

        db.session.add_all([new_package_offer_CS, new_package_offer_PO])

    elif order_type == 'PO+CS+REG':
        new_package_offer_REG = ADI_offer(assetId=asset_timestamp + '01', offer_type=params.offer_type,
                                          offerStartTime=est_params.reg_start, offerEndTime=est_params.reg_end,
                                          licenseEndTime=licenseEndTime, est_order_type='Regular',
                                          est_offerId=asset_timestamp + '01')
        db.session.add(new_package_offer_REG)

        new_package_offer_CS = ADI_offer(assetId=asset_timestamp + '01', offer_type=params.offer_type,
                                         offerStartTime=est_params.cs_start, offerEndTime=est_params.cs_end,
                                         licenseEndTime=licenseEndTime, est_order_type='ComingSoon',
                                         est_offerId=asset_timestamp + '02')
        db.session.add(new_package_offer_CS)

        new_package_offer_PO = ADI_offer(assetId=asset_timestamp + '01', offer_type=params.offer_type,
                                         offerStartTime=est_params.po_start, offerEndTime=est_params.po_end,
                                         licenseEndTime=licenseEndTime, est_order_type='PreOrder',
                                         est_offerId=asset_timestamp + '03')
        db.session.add_all([new_package_offer_REG, new_package_offer_CS, new_package_offer_PO])

    else:
        return errorchecker.internal_server_error()

    db.session.add_all([new_package_main, new_package_meta, new_package_media])
    create_purchase_options.create_po(est_pur_option, asset_timestamp)
    db.session.commit()


    return response.asset_creation_success(asset_timestamp + '01', title)



