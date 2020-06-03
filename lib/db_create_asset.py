# Filename: lib/create_tar.py
"""
Created on June 01, 2020

@author: Krishnendu Banerjee
@summary: This file holds the function for the SQLite Database Transactions

"""

from .models import ADI_main, ADI_metadata, ADI_offer, ADI_media, ADI_EST_Show, MEDIA_DEFAULT, EST_PO
from . import db
from .params_default import metadata_default_params, est_show_default_params, image_default_params

# Call Parameter Functions - These are functions to load default parameter values unless supplied in request
est_params = est_show_default_params() # Function to Load Default EST Parameters
params = metadata_default_params()  # Function to load default Param Value if Form entry is null
image_set = image_default_params()  # Function to Load Images

def add_media(provider_id, asset_type, assetId):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Creates the Database Entries for Media for any type of assets
    :access: public.
    :param provider_id: Taken from Form for Non-EST Assets; From Config for EST Assets
    :param asset_type: Type of Asset : enum: movie_config.py - default_standard_package, default_vrp_package
    :param assetId: Computed from the asset_timestamp
    :return: DB Commit in models.py - ADI_media
    """
    params.movie_details_entry(provider_id, asset_type)
    params.trailer_entry()
    image_set.image_entry(asset_type)
    path_default = MEDIA_DEFAULT.query.first()

    new_package_media = ADI_media(assetId=assetId, video_path=path_default.default_video_path,
                                  image_path=path_default.default_image_path, movie_url=params.asset_media['movie_url'],
                                  movie_checksum=params.asset_media['movie_checksum'],
                                  trailer_url=params.asset_media['trailer_file'],
                                  trailer_checksum=params.asset_media['trailer_checksum'],
                                  image_url_1=image_set.asset_image['image_1'],
                                  image_checksum_1=image_set.asset_image['image_1_checksum'],
                                  image_url_2=image_set.asset_image['image_2'],
                                  image_checksum_2=image_set.asset_image['image_2_checksum'],
                                  image_url_3=image_set.asset_image['image_3'],
                                  image_checksum_3=image_set.asset_image['image_3_checksum'],
                                  image_url_4=image_set.asset_image['image_4'],
                                  image_checksum_4=image_set.asset_image['image_4_checksum'],
                                  image_url_5=image_set.asset_image['image_5'],
                                  image_checksum_5=image_set.asset_image['image_5_checksum'],
                                  image_url_6=image_set.asset_image['image_6'],
                                  image_checksum_6=image_set.asset_image['image_6_checksum'])

    db.session.add(new_package_media)
    db.session.commit()

def add_main(assetId, asset_timestamp, adi_type, provider_version, provider_id, multiformat_id=""):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Creates the Database Entries for Main Package for any type of assets
    :access: public.
    :param assetId: Computed from the asset_timestamp
    :param asset_timestamp: asset_timestamp
    :param adi_type: Type of Asset : enum: movie_config.py - default_standard_package, default_vrp_package
    :param provider_version: Taken from form: default: 1
    :param provider_id: Taken from the form: mandatory for Non-EST, taken from movie_config for EST assets
    :param multiformat_id: optional:
    :return: DB Commit in models.py - ADI_main
    """
    new_asset_main = ADI_main(assetId=assetId, original_timestamp=asset_timestamp,
                              adi_type=adi_type, provider_version=provider_version,
                              provider_id=provider_id, multiformat_id=multiformat_id)

    db.session.add(new_asset_main)
    db.session.commit()

def add_meta(assetId, title, synopsis, par_rating, title_filter, subtitle_flag="", audio_type="", frame_rate="",
             btc_rating="", video_type="", production_year="", genre="", duration="", svod_episode_name="",
             svod_season_number="", svod_episode_number="", svod_total_episodes="", total_asset_parts="",
             dpl_template=""):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Creates the Database Entries for Metadata for package
    :access: public.
    :param assetId: Computed from asset_timestamp
    :param title: Form Input
    :param synopsis: Form Input / Computed from Title if Blank in Form
    :param par_rating: Optional Form Entry, Mandatory for Function - Default loaded from metadata_default_params
    :param title_filter: Mandatory Back End Data - Autopopulated Based on Asset type for enabling search
    :param subtitle_flag: optional: Nullable, Default loaded from metadata_default_params
    :param audio_type: optional: Nullable, Default loaded from metadata_default_params
    :param frame_rate: optional: Nullable, Default loaded from metadata_default_params
    :param btc_rating: optional: Nullable, Default loaded from metadata_default_params
    :param video_type: optional: Nullable, Default loaded from metadata_default_params
    :param production_year: optional: Nullable, Default loaded from metadata_default_params
    :param genre: optional: Nullable, Default loaded from metadata_default_params
    :param duration: optional: Nullable, Default loaded from metadata_default_params
    :param svod_episode_name: Nullable, Default loaded from metadata_default_params
    :param svod_season_number: Nullable, Default loaded from metadata_default_params
    :param svod_episode_number: Nullable, Default loaded from metadata_default_params
    :param svod_total_episodes: Nullable, Default loaded from metadata_default_params
    :param total_asset_parts: Nullable, Default loaded from metadata_default_params
    :param dpl_template: optional: Nullable, Default loaded from metadata_default_params
    :return: DB Commit in models.py - ADI_metadata
    """
    new_asset_meta = ADI_metadata(assetId=assetId, title=title, synopsis=synopsis, par_rating=par_rating,
                                  title_filter=title_filter, subtitle_flag=subtitle_flag,
                                  audio_type=audio_type, frame_rate=frame_rate, btc_rating=btc_rating,
                                  video_type=video_type, production_year=production_year, genre=genre,
                                  duration=duration, svod_episode_name=svod_episode_name,
                                  svod_season_number=svod_season_number, svod_episode_number=svod_episode_number,
                                  svod_total_episodes=svod_total_episodes, total_asset_parts=total_asset_parts,
                                  dpl_template=dpl_template)

    db.session.add(new_asset_meta)
    db.session.commit()

def add_offer(assetId, offer_type, offerStartTime, offerEndTime, licenseEndTime, service_key="", epgTime="",
              est_offerId="", est_order_type=""):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Creates the Database Entries for Offers for Packages
    :access: public.
    :param assetId: Computed from asset_timestamp
    :param offer_type: Mandatory for EST Asset - For other Asset Types loaded from metadata_default_params
    :param offerStartTime: Calculated from Current Timestamp
    :param offerEndTime: Calculated from the form_entry
    :param licenseEndTime: Calculated from the form_entry
    :param service_key: Nullable; Form Input
    :param epgTime: Computed from offerStartTime
    :param est_offerId: System Generated from asset_timestamp - mandatory for EST, null for other asset types
    :param est_order_type: Mandatory for EST, null for other asset types
    :return: DB Commit in models.py - ADI_offer
    """

    new_asset_offer = ADI_offer(assetId=assetId, offer_type=offer_type, offerStartTime=offerStartTime,
                                offerEndTime=offerEndTime, licenseEndTime=licenseEndTime, service_key=service_key,
                                epgTime=epgTime, est_offerId=est_offerId, est_order_type=est_order_type)

    db.session.add(new_asset_offer)
    db.session.commit()


def add_group(assetId, title, show_type, no_of_seasons="", no_of_episodes="", season_number="", episode_number="",
              parent_group_id=""):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Creates the Database Entries for Groups for EST Box-Sets
    :access: public.
    :param assetId: Computed from asset_timestamp
    :param title: Mandatory: Form Input
    :param show_type: Mandatory from form : TV/ Movie Box Set
    :param no_of_seasons: Mandatory for EST Shows (default est value = 1, null for other asset types)
    :param no_of_episodes: Mandatory for EST Shows (default est value = 2, null for other asset types)
    :param season_number: Computed based on form inputs for EST Shows, null for other asset types
    :param episode_number: Computed based on form inputs for EST Shows, null for other asset types
    :param parent_group_id: Computed from the asset_timestamp for Seasons and Episodes only
    :return: DB Commit in models.py - ADI_EST_Show
    """


    new_asset_group = ADI_EST_Show(assetId=assetId, title=title, show_type=show_type, no_of_seasons=no_of_seasons,
                                   no_of_episodes=no_of_episodes, season_number=season_number,
                                   episode_number=episode_number, parent_group_id=parent_group_id)

    db.session.add(new_asset_group)
    db.session.commit()


def add_purchase_option(assetId, poption_Id, poption_media_type, poption_media_filter, uk_std_price, uk_vip_price,
                        il_std_price, il_vip_price):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Creates the Database Entries for Purchase Options for EST Assets
    :access: public.
    :param assetId: Computed from asset_timestamp
    :param poption_Id: Computed from asset_timestamp
    :param poption_media_type: Form Input Digital Only/Digital+DVD/Digital+DVD+BluR
    :param poption_media_filter: Computed from poption_media_type
    :param uk_std_price: Taken from lib/movie_config.py
    :param uk_vip_price: Taken from lib/movie_config.py
    :param il_std_price: Taken from lib/movie_config.py
    :param il_vip_price: Taken from lib/movie_config.py
    :return:
    """

    new_asset_po = EST_PO(assetId=assetId, poption_Id=poption_Id, poption_media_type=poption_media_type,
                          poption_media_filter=poption_media_filter, uk_std_price=uk_std_price,
                          uk_vip_price=uk_vip_price, il_std_price=il_std_price, il_vip_price=il_vip_price)

    db.session.add(new_asset_po)
    db.session.commit()
