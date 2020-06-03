# Filename lib/create_asset.py
"""
Created on Nov 29, 2019

@author: Krishnendu Banerjee
@summary: This file holds the functions to transfer files from local to tank and vice versa:

"""
# This module creates the database entries for different type of assets
from sqlalchemy.orm.session import make_transient
from .models import ADI_main, ADI_metadata, ADI_offer
from . import db, response, create_est_offer_order
from .params_default import *
from .db_create_asset import add_media, add_main, add_meta, add_offer, add_group

# Call Parameter Functions - These are functions to load default parameter values unless supplied in request
est_params = est_show_default_params() # Function to Load Default EST Parameters
form_input = form_input_params() # Function to Load Default HTML Form Parameters
params = metadata_default_params()  # Function to load default Param Value if Form entry is null
image_set = image_default_params()  # Function to Load Images
sitemap = sitemap_mapper()  # Function to pick Jinja template based on Asset Types


def create_single_title():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Creates the Database Entries for Any type of Single Title except EST.
    :access: public.
    :return: Success Response(response.py) OR Failure(errorchecker.py)
    """
    asset_type = request.form.get('asset_type')
    if (asset_type not in movie_config.default_standard_package) and \
            (asset_type not in movie_config.default_vrp_package):
        return errorchecker.not_supported_asset_type(asset_type)  # Asset type validation
    params.set_asset_base() # This assigns the asset an assetID and offer timestamps
    form_input.get_form_values()
    params.multiformat_entry(form_input.asset_form_input['multiformat_id'],params.asset_main['asset_timestamp'])
    params.param_logic_entry(asset_type)
    params.genre_entry(asset_type)
    params.svod_episode_entry(form_input.asset_form_input['svod_season_number'],
                              form_input.asset_form_input['svod_episode_number'],
                              form_input.asset_form_input['svod_total_episodes'], asset_type,
                              form_input.asset_form_input['title'])  # Only used for Episodes
    params.dpl_entry(form_input.asset_form_input['dpl_asset_parts'], asset_type,
                     params.asset_main['asset_timestamp']) # Only for DPL Assets
    params.video_type_entry(form_input.asset_form_input['provider_id'])
    params.offer_type_entry(asset_type)

    if (form_input.asset_form_input['service_key'] == "") and ('CATCHUP' in asset_type):  # Catchup Missing Input Parameter Check
        return errorchecker.input_missing('service_key')

    # Calling DB entry creation function
    try:

        add_main(params.asset_main['asset_timestamp'] + '01', params.asset_main['asset_timestamp'], asset_type,
                 params.asset_main['provider_version'], form_input.asset_form_input['provider_id'],
                 params.asset_main['multiformat_id'])

        add_meta(params.asset_main['asset_timestamp'] + '01', form_input.asset_form_input['title'],
                 params.asset_meta['synopsis'], params.asset_meta['par_rating'], 'true',
                 params.asset_meta['subtitle_flag'], params.asset_meta['audio_type'],
                 params.asset_meta['frame_rate'], params.asset_meta['ca_btc'],
                 params.asset_meta['video_type'], params.asset_meta['production_year'],
                 params.asset_meta['genre'], params.asset_meta['runtime'], params.asset_meta['svod_episode_name'],
                 params.asset_meta['svod_season_number'], params.asset_meta['svod_episode_number'],
                 params.asset_meta['svod_total_episodes'], params.asset_meta['dpl_asset_parts'],
                 params.asset_meta['dpl_template'])

        add_offer(params.asset_main['asset_timestamp'] + '01', params.asset_meta['offer_type'],
                  params.asset_main['offerStartTime'], params.asset_main['offerEndTime'],
                  params.asset_main['licenseEndTime'], form_input.asset_form_input['service_key'],
                  epgTime=params.asset_main['offerStartTime'])

        add_media(form_input.asset_form_input['provider_id'], asset_type, params.asset_main['asset_timestamp'] + '01')

    except:  # Handling DB error
        return errorchecker.internal_server_error()

    return response.asset_creation_success(params.asset_main['asset_timestamp'] + '01',
                                           form_input.asset_form_input['title'])



def create_est_show_adi():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Creates the Database Entries for EST Shows (TV and Movie Box-Sets)
    :access: public.
    :return: Success Response(response.py) OR Failure(errorchecker.py)
    """
    params.set_asset_base()  # This assigns the asset an assetID and offer timestamps
    form_input.get_form_values()
    est_params.est_show_type_entry(form_input.asset_form_input['est_show_type'], form_input.asset_form_input['title'])
    est_params.est_series_count(form_input.asset_form_input['seasons'], form_input.asset_form_input['no_of_episodes'])
    params.param_logic_entry('est_show')
    params.offer_type_entry('est_show')
    int_timestamp = int(params.asset_main['asset_timestamp'])
    # Season Details
    for season in range(1, int(est_params.no_of_seasons) + 1):
        season_asset_id = str(int_timestamp + season)
        season_title = form_input.asset_form_input['title'] + ':S:' + str(season)
        season_synopsis = season_title + ' Synopsis'
        # Episode Details
        for episode in range(1, int(est_params.no_of_episodes) +1):
            episode_asset_id = str(int_timestamp + (season*100) + episode)
            est_params.est_show_type_entry(form_input.asset_form_input['est_show_type'], season_title)
            episode_title = est_params.est_episode_title + str(episode)
            episode_synopsis = episode_title + ' Synopsis'
            # Calling DB entry creation function
            try:
                add_main(episode_asset_id + '22', episode_asset_id + '22', 'est_episode',
                         params.asset_main['provider_version'], est_params.est_episode_provider)

                add_meta(episode_asset_id + '22', episode_title, episode_synopsis, params.asset_meta['par_rating'],
                         'false', btc_rating=params.asset_meta['ca_btc'])

                add_media(est_params.est_episode_provider, 'est_episode', episode_asset_id + '22')

                add_group(episode_asset_id + '22', episode_title, form_input.asset_form_input['est_show_type'],
                          season_number=str(season), episode_number=str(episode), parent_group_id=season_asset_id + '11')

                add_offer(episode_asset_id + '22', params.asset_meta['offer_type'], params.asset_main['offerStartTime'],
                          params.asset_main['licenseEndTime'], params.asset_main['licenseEndTime'])

            except:
                errorchecker.internal_server_error_show('EST_EPISODE')

        try:
            add_main(season_asset_id + '11', season_asset_id + '11', 'est_season',
                     params.asset_main['provider_version'], 'est__season_hd')

            add_meta(season_asset_id + '11', season_title, season_synopsis, params.asset_meta['par_rating'],
                     'false', btc_rating=params.asset_meta['ca_btc'])

            add_offer(season_asset_id + '11', params.asset_meta['offer_type'], params.asset_main['offerStartTime'],
                          params.asset_main['licenseEndTime'], params.asset_main['licenseEndTime'])

            add_group(season_asset_id + '11', season_title, form_input.asset_form_input['est_show_type'],
                      no_of_episodes=est_params.no_of_episodes, season_number=str(season),
                      parent_group_id=params.asset_main['asset_timestamp'] + '00')

        except:
            errorchecker.internal_server_error_show('EST_SEASON')

    try:
        add_main(params.asset_main['asset_timestamp'] + '00', params.asset_main['asset_timestamp'],
                 'est_show', params.asset_main['provider_version'], est_params.est_show_provider)

        add_meta(params.asset_main['asset_timestamp'] + '00', form_input.asset_form_input['title'],
                 params.asset_meta['synopsis'], params.asset_meta['par_rating'], 'true',
                 btc_rating=params.asset_meta['ca_btc'])

        add_media(est_params.est_show_provider, 'est_show', params.asset_main['asset_timestamp'] + '00')

        add_group(params.asset_main['asset_timestamp'] + '00', form_input.asset_form_input['title'],
                  form_input.asset_form_input['est_show_type'], no_of_seasons= est_params.no_of_seasons,
                  no_of_episodes=est_params.no_of_episodes)

        # Creating EST ORDER TYPE to specify if Offer is Regular / Coming Soon / PreOrder
        create_est_offer_order.create_est_orders(params.asset_main['asset_timestamp'], params.asset_main['licenseEndTime'],
                                                form_input.asset_form_input['order_type'], 'est_show')

        # Create the Purchase Options to specify the Purchase Option is (BluRay/Digital/DVD)
        create_est_offer_order.create_po(form_input.asset_form_input['po_type'], params.asset_main['asset_timestamp'],
                                          'est_show')
    except:
        errorchecker.internal_server_error_show('EST_SHOW')


    return response.asset_creation_success(params.asset_main['asset_timestamp'] + '00',
                                           form_input.asset_form_input['title'])





def create_est_title_adi():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Creates the Database Entries for EST Single Titles
    :access: public.
    :return: Success Response(response.py) OR Failure(errorchecker.py)
    """
    params.set_asset_base()  # This assigns the asset an assetID and offer timestamps
    form_input.get_form_values()
    params.param_logic_entry('EST SINGLE TITLE')
    params.video_type_entry(movie_config.est_title_provider)
    params.offer_type_entry('EST SINGLE TITLE')

    add_main(params.asset_main['asset_timestamp'] + '01', params.asset_main['asset_timestamp'],
             'EST SINGLE TITLE', params.asset_main['provider_version'], movie_config.est_title_provider)

    add_meta(params.asset_main['asset_timestamp'] + '01', form_input.asset_form_input['title'],
             params.asset_meta['synopsis'], params.asset_meta['par_rating'], 'true',
             params.asset_meta['subtitle_flag'], params.asset_meta['audio_type'],
             params.asset_meta['frame_rate'], params.asset_meta['ca_btc'],
             params.asset_meta['video_type'], params.asset_meta['production_year'],
             duration=params.asset_meta['runtime'])

    add_media(movie_config.est_title_provider, 'EST SINGLE TITLE', params.asset_main['asset_timestamp'] + '01')

    # Creating EST ORDER TYPE to specify if Offer is Regular / Coming Soon / PreOrder
    create_est_offer_order.create_est_orders(params.asset_main['asset_timestamp'], params.asset_main['licenseEndTime'],
                                            form_input.asset_form_input['order_type'], 'EST SINGLE TITLE')

    # Create the Purchase Options to specify the Purchase Option is (BluRay/Digital/DVD)
    create_est_offer_order.create_po(form_input.asset_form_input['po_type'], params.asset_main['asset_timestamp'],
                                      'EST SINGLE TITLE')

    return response.asset_creation_success(params.asset_main['asset_timestamp'] + '01',
                                           form_input.asset_form_input['title'])



# This function Clones already Created Assets # Cloning Not Supported For EST Titles and Box-Sets
def clone_asset():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Clones already Created Assets
    :access: public.
    :return: Success Response(response.py) OR Failure(errorchecker.py)
    :except: asset_types: EST Single Title and Box-Set
    """
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
    return response.asset_creation_success(asset_timestamp + '01', title)







