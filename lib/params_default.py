# Filename: lib/params_default.py
"""
Created on June 01, 2020

@author: Krishnendu Banerjee
@summary: This file holds the classes for Default inputs for Forms, Metadata and EST parameters
"""

from . import movie_config, errorchecker, offerdate
from flask import request
from .models import MEDIA_LIBRARY, MEDIA_DEFAULT, ADI_media
import datetime, time

class form_input_params(object):
    """
    Class to initiate the default Form Input Parameters
    """
    def __init__(self):
        self.asset_form_input = {}

    def get_form_values(self):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to initiate common form fields
        :access: public.
        :return: Initiate Parameters
        """
        self.asset_form_input['provider_id'] = request.form.get('provider_id')
        self.asset_form_input['title'] = request.form.get('title')
        self.asset_form_input['service_key'] = request.form.get('service_key')
        self.asset_form_input['multiformat_id'] = request.form.get('multiformat_id')
        self.asset_form_input['svod_season_number'] = request.form.get('svod_season_number')
        self.asset_form_input['svod_episode_number'] = request.form.get('svod_episode_number')
        self.asset_form_input['svod_total_episodes'] = request.form.get('svod_total_episodes')
        self.asset_form_input['dpl_asset_parts'] = request.form.get('dpl_asset_parts')
        self.asset_form_input['order_type'] = request.form.get('order_type')
        self.asset_form_input['po_type'] = request.form.get('po_type')
        self.asset_form_input['est_show_type'] = request.form.get('est_show_type')
        self.asset_form_input['seasons'] = request.form.get('seasons')
        self.asset_form_input['no_of_episodes'] = request.form.get('no_of_episodes')


class est_show_default_params(object):
    """
    Class to initiate default EST Show / Single Title input parameters
    """

    def __init__(self):
        self.purchase_option_params = {}
        self.est_show_provider = None
        self.est_episode_provider = None
        self.est_episode_title = None
        self.no_of_seasons = None
        self.no_of_episodes = None

    def est_show_type_entry(self, show_type, title):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to Initiate the Show/Season/Episode Default parameters
        :access: public.
        :param show_type: Specify whether TV Box-Set or Movie Box-Set
        :param title:
        :return: Initiate the Show/Season/Episode Default parameters
        """
        if show_type == 'Movie BS':
            self.est_show_provider = movie_config.movie_show_provider
            self.est_episode_provider = movie_config.movie_episode_provider
            self.est_episode_title = title + ':Mov:'
        else:
            self.est_show_provider = movie_config.tv_show_provider
            self.est_episode_provider = movie_config.tv_episode_provider
            self.est_episode_title = title + ':Ep:'

    def est_series_count(self, no_of_seasons, no_of_episodes):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to Initiate the No of Seasons/Episodes for EST Box-Sets
        :access: public.
        :param no_of_seasons: Specify the Number of Seasons for EST Box-Sets
        :param no_of_episodes: Specify the Number of Episodes for EST Box-Sets
        :return: Initiate the No of Seasons/Episodes for EST Box-Sets
        """
        if no_of_seasons == "":
            self.no_of_seasons = movie_config.default_no_of_seasons
        else:
            self.no_of_seasons = no_of_seasons
        if no_of_episodes == "":
            self.no_of_episodes = movie_config.default_no_of_episodes
        else:
            self.no_of_episodes = no_of_episodes

    def est_offer_window_entry(self, po_offer_window, cs_offer_window, reg_offer_window):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to Initiate the Default Offer Windows for EST Assets
        :access: public.
        :param po_offer_window: Initiate default pre-order offer window for EST Assets
        :param cs_offer_window: Initiate default comingSoon offer window for EST Assets
        :param reg_offer_window: Initiate default Regular offer window for EST Assets
        :return: Default Offer Window
        """
        if po_offer_window != "":
            self.purchase_option_params['po_offer_window'] = po_offer_window
        else:
            self.purchase_option_params['po_offer_window'] = '7'

        if cs_offer_window != "":
            self.purchase_option_params['cs_offer_window'] = cs_offer_window
        else:
            self.purchase_option_params['cs_offer_window'] = '7'

        if reg_offer_window != "":
            self.purchase_option_params['reg_offer_window'] = reg_offer_window
        else:
            self.purchase_option_params['reg_offer_window'] = '30'

    def est_offer_date_entry(self, order_type, po_offer_window, cs_offer_window, reg_offer_window):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to Initiate the Default Offer Dates for EST Assets
        :access: public.
        :param order_type:
        :param po_offer_window: Initiate default pre-order offer date for EST Assets
        :param cs_offer_window: Initiate default ComingSoon offer window for EST Assets
        :param reg_offer_window: Initiate default Regular offer window for EST Assets
        :return: Default Offer Dates
        """
        if order_type == "PO":
            self.purchase_option_params['po_start'] = offerdate.offer_date(0, 0)
            self.purchase_option_params['po_end'] = offerdate.offer_date(int(po_offer_window), 0)
        elif order_type == "PO+CS":
            po_cs_window = int(po_offer_window) + int(cs_offer_window)
            self.purchase_option_params['po_start'] = offerdate.offer_date(0, 0)
            self.purchase_option_params['po_end'] = offerdate.offer_date(int(po_offer_window), 0)
            self.purchase_option_params['cs_start'] = offerdate.offer_date(int(po_offer_window), 1)
            self.purchase_option_params['cs_end'] = offerdate.offer_date(po_cs_window, 0)
        elif order_type == "REG":
            self.purchase_option_params['reg_start'] = offerdate.offer_date(0, 0)
            self.purchase_option_params['reg_end'] = offerdate.offer_date(int(reg_offer_window), 0)
        elif order_type == "PO+CS+REG":
            po_cs_window = int(po_offer_window) + int(cs_offer_window)
            po_cs_reg_window = int(po_offer_window) + int(cs_offer_window) + int(reg_offer_window)
            self.purchase_option_params['po_start']  = offerdate.offer_date(0, 0)
            self.purchase_option_params['po_end']  = offerdate.offer_date(int(po_offer_window), 0)
            self.purchase_option_params['cs_start'] = offerdate.offer_date(int(po_offer_window), 1)
            self.purchase_option_params['cs_end']  = offerdate.offer_date(po_cs_window, 0)
            self.purchase_option_params['reg_start']  = offerdate.offer_date(po_cs_window, 1)
            self.purchase_option_params['reg_end']  = offerdate.offer_date(po_cs_reg_window, 0)


class image_default_params(object):
    """
    Class to initiate the default image parameters
    """

    def __init__(self):
        self.asset_image = {}

    def get_checksum(self, filename):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to calculate checksum
        :access: public.
        :param filename: Specify the Filename for which the checksum needs to be calculated
        :return: Checksum
        """
        file = MEDIA_LIBRARY.query.filter_by(filename=filename).first()
        return file.checksum

    def image_entry(self, asset_type):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to Initiate the Media types for Assets
        :access: public.
        :param asset_type: Specify the Asset Type for which the Media needs to be specified (DPL/Standard)
        :return: Initiate the Media types for DPL/Standard Assets
        """
        image_path_default = MEDIA_DEFAULT.query.first()
        if 'DPL' in asset_type:
            if request.form.get('image_group') == "":
                file_pref = image_path_default.dpl_image_file_prefix
            else:
                file_pref = request.form.get('image_group')
            self.asset_image['image_1'] = file_pref + '_THUM.jpg'
            self.asset_image['image_2']  = file_pref + '_CATI.jpg'
            self.asset_image['image_3']  = file_pref + '_PRAW.jpg'
            self.asset_image['image_4']  = file_pref + '_PRIW.jpg'
            self.asset_image['image_5']  = file_pref + '_PRSW.jpg'
            self.asset_image['image_6']  = file_pref + '_PRMW.jpg'
            self.asset_image['image_1_checksum'] = self.get_checksum(self.asset_image['image_1'])
            self.asset_image['image_2_checksum'] = self.get_checksum(self.asset_image['image_2'])
            self.asset_image['image_3_checksum'] = self.get_checksum(self.asset_image['image_3'])
            self.asset_image['image_4_checksum'] = self.get_checksum(self.asset_image['image_4'])
            self.asset_image['image_5_checksum'] = self.get_checksum(self.asset_image['image_5'])
            self.asset_image['image_6_checksum'] = self.get_checksum(self.asset_image['image_6'])
        else:
            if request.form.get('image_group') == "":
                file_pref = image_path_default.standard_image_file_prefix
            else:
                file_pref = request.form.get('image_group')
            self.asset_image['image_1'] = file_pref + '_182x98.jpg'
            self.asset_image['image_2'] = file_pref + '_182x243.jpg'
            self.asset_image['image_3'] = file_pref + '_262x349.jpg'
            self.asset_image['image_4'] = file_pref + '_456x257.jpg'
            self.asset_image['image_5'] = ""
            self.asset_image['image_6'] = ""
            self.asset_image['image_1_checksum'] = self.get_checksum(self.asset_image['image_1'])
            self.asset_image['image_2_checksum'] = self.get_checksum(self.asset_image['image_2'])
            self.asset_image['image_3_checksum'] = self.get_checksum(self.asset_image['image_3'])
            self.asset_image['image_4_checksum'] = self.get_checksum(self.asset_image['image_4'])
            self.asset_image['image_5_checksum'] = ""
            self.asset_image['image_6_checksum'] = ""


class metadata_default_params(object):
    """
    Class to initiate the default metadata for assets
    """

    def __init__(self):
        self.asset_main = {}
        self.asset_meta = {}
        self.asset_media = {}
        self.environment_url = None
        self.tank_path = None

    def set_asset_base(self):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to Initiate offerEndDateTime
        :access: public.
        :return: OfferEndDateTime in ADI format
        """
        ts = time.time()
        self.asset_main['asset_timestamp'] = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')  # Setting current timestamp
        self.asset_main['licenseEndTime'] = offerdate.offer_date(int(request.form.get('LicenseWindow')), 0)  # Adding Window days from now
        self.asset_main['offerStartTime'] = offerdate.offer_date(0, 0)  # Setting Offer Start Time to now
        if request.form.get('offer_window') != None:
            self.asset_main['offerEndTime'] = offerdate.offer_date(int(request.form.get('offer_window')), 0)
        else:
            self.asset_main['offerEndTime'] = ""


    def param_logic_entry(self, asset_type):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to Initiate the Default Asset Metadata based on Asset_Type
        :access: public.
        :param asset_type: As per Movie_Config.py
        :return:
        """
        if request.form.get('synopsis') != "":
            self.asset_meta['synopsis'] = request.form.get('synopsis')
        else:
            self.asset_meta['synopsis'] = movie_config.default_synopsis + request.form.get('title')

        if request.form.get('provider_version') != "":
            self.asset_main['provider_version'] = request.form.get('provider_version')
        else:
            self.asset_main['provider_version'] = movie_config.default_provider_version

        if request.form.get('production_year') != "":
            self.asset_meta['production_year'] = request.form.get('production_year')
        else:
            self.asset_meta['production_year'] = movie_config.default_production_year

        if request.form.get('ca_btc') != "":
            self.asset_meta['ca_btc'] = request.form.get('ca_btc')
        elif request.form.get('ca_btc') == "" and 'PREMIUM VOD' in asset_type:
            self.asset_meta['ca_btc'] = '31'
        else:
            self.asset_meta['ca_btc'] = movie_config.default_ca_btc

        if request.form.get('par_rating') != "":
            self.asset_meta['par_rating'] = request.form.get('par_rating')
        else:
            self.asset_meta['par_rating'] = movie_config.default_par_rating

        if request.form.get('audio_type') != "":
            self.asset_meta['audio_type'] = request.form.get('audio_type')
        else:
            self.asset_meta['audio_type'] = movie_config.default_audio_type

        if request.form.get('frame_rate') != "":
            self.asset_meta['frame_rate']= request.form.get('frame_rate')
        else:
            self.asset_meta['frame_rate'] = movie_config.default_frame_rate

        if request.form.get('subtitle_flag') != "":
            self.asset_meta['subtitle_flag'] = request.form.get('subtitle_flag')
        else:
            self.asset_meta['subtitle_flag']  = movie_config.default_subtitle_flag

        if request.form.get('duration') != "" and 'est' not in asset_type:
            self.asset_meta['runtime']  = request.form.get('duration')
            self.asset_meta['duration']  = 'PT'+(request.form.get('duration')).split(':')[0]+'H'+\
                            (request.form.get('duration')).split(':')[1]+'M'+(request.form.get('duration')).split(':')[2]+'S'
        else:
            self.asset_meta['runtime'] = movie_config.default_asset_runtime
            self.asset_meta['duration'] = movie_config.default_asset_duration

    def genre_entry(self, asset_type):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to Initiate Genre based on Asset_Type
        :access: public.
        :param asset_type:
        :return: Initiate Genre based on Asset_Type
        """
        if request.form.get('genre') != "":
            self.asset_meta['genre'] = request.form.get('genre')
        elif request.form.get('genre') == "" and 'EPISODE' in asset_type:
            self.asset_meta['genre'] = movie_config.default_episode_genre
        else:
            self.asset_meta['genre'] = movie_config.default_movie_genre


    def get_checksum(self, filename):
        file = MEDIA_LIBRARY.query.filter_by(filename=filename).first()
        return file.checksum

    def multiformat_entry(self, multiformat_id, asset_timestamp):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to Initiate multiformat ID if null in Form
        :access: public.
        :param multiformat_id: Form Entry
        :param asset_timestamp: Calculated
        :return: multiformatId
        """
        if multiformat_id != "":
            self.asset_main['multiformat_id'] = multiformat_id
        else:
            self.asset_main['multiformat_id'] = 'BSKYPR' + asset_timestamp

    def movie_details_entry(self, provider_id, asset_type):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to Initiate Movie URL based on ProviderID and AssetType
        :access: public.
        :param provider_id: Form input
        :param asset_type: Form input (based on Movie_Config.py
        :return: default movie url based on ProviderID and AssetType
        """
        url_default = MEDIA_DEFAULT.query.first()
        if request.form.get('video_file') == "":
            if 'hdr' in provider_id and 'DPL' not in asset_type:
                self.asset_media['movie_url'] = url_default.hdr_movie_file
            elif '4k' in provider_id and 'DPL' not in asset_type:
                self.asset_media['movie_url'] = url_default.sdr_movie_file
            elif 'est' in provider_id and 'DPL' not in asset_type:
                self.asset_media['movie_url'] = url_default.est_movie_file
            elif (('hd.' in provider_id) or ('_hd' in provider_id)) and 'DPL' not in asset_type:
                self.asset_media['movie_url'] = url_default.hd_movie_file
            elif 'DPL' in asset_type:
                self.asset_media['movie_url'] = url_default.dpl_movie_file
            elif 'SECONDARY' in asset_type:
                self.asset_media['movie_url'] = url_default.trailer_file
            else:
                self.asset_media['movie_url'] = url_default.title_movie_file
        else:
            self.asset_media['movie_url'] = request.form.get('video_file')

        try:
            self.asset_media['movie_checksum'] = self.get_checksum(self.asset_media['movie_url'])
        except AttributeError:
            return errorchecker.missing_file_libary(self.asset_media['movie_url'])


    def trailer_entry(self):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to Initiate Trailer URL
        :access: public.
        :return: default trailer URL
        """
        trailer_default = MEDIA_DEFAULT.query.first()
        self.asset_media['trailer_file'] = trailer_default.trailer_file
        try:
            self.asset_media['trailer_checksum'] = self.get_checksum(self.asset_media['trailer_file'])
        except AttributeError:
            return errorchecker.missing_file_libary(self.asset_media['trailer_file'])

    def video_type_entry(self, provider_id):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to Initiate video type based on ProviderID
        :access: public.
        :param provider_id: Form input
        :return: movie_type (HD true or false)
        """
        if ('hdr' in provider_id) or ('4k' in provider_id) or ('hd.' in provider_id) or ('_hd' in provider_id):
            self.asset_meta['video_type'] = 'true'
        else:
            self.asset_meta['video_type'] = 'false'

    def offer_type_entry(self, asset_type):
        if 'RENTAL' in asset_type or 'PREMIUM' in asset_type or 'EST' in asset_type:
            self.asset_meta['offer_type'] = 'IPPR'
        elif 'est' in asset_type:
            self.asset_meta['offer_type'] = 'IPPR'
        else:
            self.asset_meta['offer_type'] = 'SVOD'

    def svod_episode_entry(self, svod_season_number, svod_episode_number, svod_total_episodes, asset_type, title):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to Initiate series information of Non-EST assets (SVOD/CUTV/DPL Episodes)
        :access: public.
        :param svod_season_number: Form_input: Initiate default param for Non-EST Asset if null
        :param svod_episode_number: Form_input: Initiate default param for Non-EST Asset if null
        :param svod_total_episodes: Form_input: Initiate default param for Non-EST Asset if null
        :param asset_type: Form_input; Based on movie_config.py
        :param title: Form_input
        :return: Initiate series information of Non-EST assets (SVOD/CUTV/DPL Episodes)
        """
        if 'EPISODE' in asset_type:
            if svod_season_number != "":
                self.asset_meta['svod_season_number'] = svod_season_number
            else:
                self.asset_meta['svod_season_number'] = '1'

            if svod_episode_number != "":
                self.asset_meta['svod_episode_number'] = svod_episode_number
            else:
                self.asset_meta['svod_episode_number'] = '1'

            if svod_total_episodes != "":
                self.asset_meta['svod_total_episodes'] = svod_total_episodes
            else:
                self.asset_meta['svod_total_episodes'] = self.asset_meta['svod_episode_number']

            self.asset_meta['svod_episode_name'] = title + ',S:' + self.asset_meta['svod_season_number'] + ',Ep:' + \
                                                   self.asset_meta['svod_episode_number']

        else:
            self.asset_meta['svod_season_number'] = ""
            self.asset_meta['svod_episode_number'] = ""
            self.asset_meta['svod_total_episodes'] = ""
            self.asset_meta['svod_episode_name'] = ""




    def dpl_entry(self, dpl_asset_parts, asset_type, asset_timestamp):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to Initiate DPL asset part information for DPL Assets only
        :access: public.
        :param dpl_asset_parts: Specifies the Asset Part for DPL asset: default 2
        :param asset_type: If Standard/DPL asset
        :param asset_timestamp: Calculated from current timestamp
        :return:
        """
        if 'DPL' in asset_type:
            if dpl_asset_parts != "":
                self.asset_meta['dpl_asset_parts'] = dpl_asset_parts
            else:
                self.asset_meta['dpl_asset_parts'] = '2'

            self.asset_meta['dpl_template'] = asset_timestamp + '_template_' + self.asset_meta['dpl_asset_parts']
        else:
            self.asset_meta['dpl_asset_parts'] = ""
            self.asset_meta['dpl_template'] = ""



    def environment_entry(self, environment):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to Initiate test environment endpoint information
        :access: public.
        :param environment: Specify which Test environment the Asset will be posted and reads from movie_config.py
        :return: Environment URL
        """
        if environment == 'TS1:CMS':
            self.environment_url = movie_config.ts1_cms
        elif environment == 'TS1:VMS':
            self.environment_url = movie_config.ts1_vms
        elif environment == 'TS2:CMS':
            self.environment_url = movie_config.ts2_cms
        elif environment == 'TS2:VMS':
            self.environment_url = movie_config.ts2_vms
        elif environment == 'TS3:CMS':
            self.environment_url = movie_config.ts3_cms
        elif environment == 'TS3:VMS':
            self.environment_url = movie_config.ts3_vms
        elif environment == 'TS4:CMS':
            self.environment_url = movie_config.ts4_cms
        elif environment == 'TS4:VMS':
            self.environment_url = movie_config.ts4_vms
        elif environment == 'STAGE:CMS':
            self.environment_url = movie_config.stage_cms
        elif environment == 'STAGE:VMS':
            self.environment_url = movie_config.stage_vms
        else:
            return errorchecker.environment_not_defined(environment)


    def tank_entry(self, environment, file_type, path):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to Initiate Tank Path
        :access: public.
        :param environment:
        :param file_type: Image/Video/VRP Tar
        :param path: Path to upload media in Tank
        :return: Success Path for Tank
        """
        path_default = MEDIA_DEFAULT.query.first()
        image_path = path_default.default_image_path
        video_path = path_default.default_video_path
        if environment == 'TS1':
            if file_type == 'Image':
                self.tank_path = '/ifs/PDLTankTest/Test1/Wholesale/' + image_path
            else:
                self.tank_path = '/ifs/PDLTankTest/Test1/' + video_path
        elif environment == 'TS2':
            if file_type == 'Image':
                self.tank_path = '/ifs/PDLTankTest/Test2/Wholesale/' + image_path
            else:
                self.tank_path = '/ifs/PDLTankTest/Test2/' + video_path
        elif environment == 'TS3':
            if file_type == 'Image':
                self.tank_path = '/ifs/PDLTankTest/Test3/Wholesale/' + image_path
            else:
                self.tank_path = '/ifs/PDLTankTest/Test3/' + video_path
        elif environment == 'STAGE':
            if file_type == 'Image':
                self.tank_path = '/ifs/PDLTankTest/Wholesale/' + image_path
            else:
                self.tank_path = '/ifs/PDLTankTest/' + video_path
        elif environment == "":
            self.tank_path = path
        else:
            return errorchecker.environment_not_defined(environment)


class adi_package_logic(object):
    """
    Class to initiate the ADI Package Logic
    """

    def __init__(self):
        self.movie_path = None
        self.image_path = None
        self.asset_duration = None
        self.dpl_mid_rolls = None
        self.term_type = None

    def path_builder(self, asset_type, assetId):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to Initiate Media Path for VRP / Non-VRP assets
        :access: public.
        :param asset_type: From movie_config.py
        :param assetId: AssetId
        :return: Returns the default tank path or location for Media/Image/Trailers based on VRP Package or Non-VRP
        """
        package_media = ADI_media.query.filter_by(assetId=assetId).first()
        if 'VRP' in asset_type:
            self.image_path = ""
            self.movie_path = ""
        else:
            self.image_path = 'tank/' + package_media.image_path
            self.movie_path = package_media.video_path

    def duration_calc(self, runtime):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to calculate the duration and runtime and initiate in ADI format
        :access: public.
        :param runtime: form_input or read default from movie_config.py
        :return: duration and runtime and initiate in ADI format
        """
        self.asset_duration = 'PT' + runtime.split(':')[0] + 'H' + runtime.split(':')[1] + 'M' + runtime.split(':')[2] + 'S'

    def dpl_midroll_calc(self, asset_type, total_asset_parts):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to Calculate DPL midrolls from Asset Parts
        :access: public.
        :param asset_type: DPL/Non-DPL
        :param total_asset_parts: Specified Asset Parts from Form_input or read default = 2 from movie_config.py
        :return: calculated number of midrolls from Asset_Parts
        """
        if 'DPL' not in asset_type:
            self.dpl_mid_rolls = ""
        else:
            self.dpl_mid_rolls = str(int(total_asset_parts) - 1)

    def term_type_generate(self, asset_type):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to Initiate Term Type based on Specified Asset_Type
        :access: public.
        :param asset_type: Form_input based on movie_config.py
        :return: Return Term Type based on Asset Type
        """
        if 'CATCHUP' in asset_type:
            self.term_type = 'CUTV'
        else:
            self.term_type = 'Archive'


class sitemap_mapper(object):
    """
    Class to initiate the specific Sitemap (Jinja Template to use for specific Asset Types)
    """

    def __init__(self):
        self.sitemap = None

    def sitemap_entry(self, asset_type):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to return Specific Jinja Template XML for Assets based on the Specified Asset Type
        :access: public.
        :param asset_type: Form_input based on movie_config.py
        :return: Specific Jinja Template XML for Assets based on the Specified Asset Type
        """
        if 'DPL' not in asset_type and 'SECONDARY' not in asset_type:
            self.sitemap = 'ASSET_STANDARD_TITLE.xml'
        elif 'DPL' in asset_type:
            self.sitemap = 'ASSET_DPL_TITLE.xml'
        elif 'SECONDARY' in asset_type:
            self.sitemap = 'ASSET_SECONDARY.xml'
        else:
            self.sitemap = False


    def sitemap_entry_boxset(self, asset_type, show_type):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to return Specific Jinja EST Show Template XML for Assets based on the Specified Asset Type
        :access: public.
        :param asset_type: Form_input based on movie_config.py
        :param show_type: Form_input (TV/Movie Box-Set
        :return: Specific Jinja EST Show Template XML for Assets based on the Specified Asset Type
        """
        if asset_type == 'est_show':
            self.sitemap = 'ASSET_EST_SHOW.xml'
        elif asset_type == 'est_season':
            self.sitemap = 'ASSET_EST_SEASON.xml'
        elif asset_type == 'est_episode':
            if show_type == 'Movie BS':
                self.sitemap = 'ASSET_EST_MOVIE_EPISODE.xml'
            else:
                self.sitemap = 'ASSET_EST_EPISODE.xml'
        elif asset_type == 'EST SINGLE TITLE':
            self.sitemap = 'ASSET_EST_SINGLE_TITLE.xml'
        else:
            self.sitemap = False

    def sitemap_entry_est_title(self, asset_type):
        """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function to return Specific EST Single Title Template XML
        :access: public.
        :param asset_type: EST Single Title
        :return: Return EST Single Title Template based on Asset_Type
        """
        if asset_type == 'EST SINGLE TITLE':
            self.sitemap = 'ASSET_EST_SINGLE_TITLE.xml'
        else:
            self.sitemap = False