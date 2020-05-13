from . import movie_config, errorchecker, offerdate
from flask import request
from .models import MEDIA_LIBRARY, MEDIA_DEFAULT
import datetime, time
class metadata_default_params(object):

    def __init__(self):
        self.asset_main = {}
        self.asset_meta = {}
        self.asset_media = {}
        self.environment_url = None
        self.tank_path = None

    def set_asset_base(self):
        ts = time.time()
        self.asset_main['asset_timestamp'] = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')  # Setting current timestamp
        self.asset_main['licenseEndTime'] = offerdate.offer_date(int(request.form.get('LicenseWindow')), 0)  # Adding Window days from now
        self.asset_main['offerStartTime'] = offerdate.offer_date(0, 0)  # Setting Offer Start Time to now
        if request.form.get('offer_window') != None:
            self.asset_main['offerEndTime'] = offerdate.offer_date(int(request.form.get('offer_window')), 0)
        else:
            self.asset_main['offerEndTime'] = ""


    def param_logic_entry(self, asset_type):
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
        if multiformat_id != "":
            self.asset_main['multiformat_id'] = multiformat_id
        else:
            self.asset_main['multiformat_id'] = 'BSKYPR' + asset_timestamp

    def movie_details_entry(self, provider_id, asset_type):
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
        trailer_default = MEDIA_DEFAULT.query.first()
        self.asset_media['trailer_file'] = trailer_default.trailer_file
        try:
            self.asset_media['trailer_checksum'] = self.get_checksum(self.asset_media['trailer_file'])
        except AttributeError:
            return errorchecker.missing_file_libary(self.asset_media['trailer_file'])

    def video_type_entry(self, provider_id):
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
