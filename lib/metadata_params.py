from . import movie_config
from . import errorchecker
from .models import MEDIA_LIBRARY
class metadata_default_params(object):

    def __init__(self):
        self.synopsis = None
        self.provider_version = None
        self.production_year = None
        self.ca_btc = None
        self.par_rating = None
        self.audio_type = None
        self.frame_rate = None
        self.subtitle_flag = None
        self.multiformat_id = None
        self.movie_url = None
        self.movie_checksum = None
        self.video_type = None
        self.offer_type = None
        self.runtime = None
        self.duration = None
        self.environment_url = None
        self.svod_season_number = None
        self.svod_episode_number = None
        self.svod_total_episodes = None
        self.svod_episode_name = None
        self.dpl_asset_parts = None
        self.dpl_template = None
        self.trailer_file = None
        self.trailer_checksum = None

    def param_logic_entry(self, synopsis, title, provider_version, production_year, ca_btc, par_rating, audio_type,
                          frame_rate, subtitle_flag, asset_duration):
        if synopsis != "":
            self.synopsis = synopsis
        else:
            self.synopsis = movie_config.default_synopsis + title

        if provider_version != "":
            self.provider_version = provider_version
        else:
            self.provider_version = movie_config.default_provider_version

        if production_year != "":
            self.production_year = production_year
        else:
            self.production_year = movie_config.default_production_year

        if ca_btc != "":
            self.ca_btc = ca_btc
        else:
            self.ca_btc = movie_config.default_ca_btc

        if par_rating != "":
            self.par_rating = par_rating
        else:
            self.par_rating = movie_config.default_par_rating

        if audio_type != "":
            self.audio_type = audio_type
        else:
            self.audio_type = movie_config.default_audio_type

        if frame_rate != "":
            self.frame_rate = frame_rate
        else:
            self.frame_rate = movie_config.default_frame_rate

        if subtitle_flag != "":
            self.subtitle_flag = subtitle_flag
        else:
            self.subtitle_flag = movie_config.default_subtitle_flag

        if asset_duration != "":
            self.runtime = asset_duration
            self.duration = 'PT'+asset_duration.split(':')[0]+'H'+asset_duration.split(':')[1]+'M'+asset_duration.split(':')[2]+'S'
        else:
            self.runtime = movie_config.default_asset_runtime
            self.duration = movie_config.default_asset_duration

    def get_checksum(self, filename):
        file = MEDIA_LIBRARY.query.filter_by(filename=filename).first()
        return file.checksum

    def multiformat_entry(self, multiformat_id, asset_timestamp):
        if multiformat_id != "":
            self.multiformat_id = multiformat_id
        else:
            self.multiformat_id = 'BSKYPR' + asset_timestamp

    def movie_details_entry(self, provider_id, asset_type):
        if 'hdr' in provider_id and 'DPL' not in asset_type:
            self.movie_url = movie_config.hdr_movie_file
        elif '4k' in provider_id and 'DPL' not in asset_type:
            self.movie_url = movie_config.sdr_movie_file
            # self.movie_checksum = movie_config.sdr_movie_checksum
        elif 'est' in provider_id and 'DPL' not in asset_type:
            self.movie_url = movie_config.est_movie_file
        elif (('hd.' in provider_id) or ('_hd' in provider_id)) and 'DPL' not in asset_type:
            self.movie_url = movie_config.hd_movie_file
        elif 'DPL' in asset_type:
            self.movie_url = movie_config.dpl_movie_url
        else:
            self.movie_url = movie_config.title_movie

        try:
            self.movie_checksum = self.get_checksum(self.movie_url)
        except AttributeError:
            return errorchecker.missing_file_libary(self.movie_url)


    def trailer_entry(self):
        self.trailer_file = movie_config.trailer_file
        try:
            self.trailer_checksum = self.get_checksum(self.trailer_file)
        except AttributeError:
            return errorchecker.missing_file_libary(self.trailer_file)

    def video_type_entry(self, provider_id):
        if ('hdr' in provider_id) or ('4k' in provider_id) or ('hd.' in provider_id) or ('_hd' in provider_id):
            self.video_type = 'true'
        else:
            self.video_type = 'false'

    def offer_type_entry(self, asset_type):
        if 'RENTAL' in asset_type or 'PREMIUM' in asset_type:
            self.offer_type = 'IPPR'
        elif 'est' in asset_type:
            self.offer_type = 'IPPR'
        else:
            self.offer_type = 'SVOD'

    def svod_episode_entry(self, svod_season_number, svod_episode_number, svod_total_episodes, asset_type, title):
        if 'EPISODE' in asset_type:
            if svod_season_number != "":
                self.svod_season_number = svod_season_number
            else:
                self.svod_season_number = '1'

            if svod_episode_number != "":
                self.svod_episode_number = svod_episode_number
            else:
                self.svod_episode_number = '1'

            if svod_total_episodes != "":
                self.svod_total_episodes = svod_total_episodes
            else:
                self.svod_total_episodes = svod_episode_number

            self.svod_episode_name = 'EpisodeName for: ' + title + ', Season: ' + self.svod_season_number + ', Episode: ' \
                                     + self.svod_episode_number

        else:
            self.svod_season_number = ""
            self.svod_episode_number = ""
            self.svod_total_episodes = ""
            self.svod_episode_name = ""




    def dpl_entry(self, dpl_asset_parts, asset_type, asset_timestamp):
        if 'DPL' in asset_type:
            if dpl_asset_parts != "":
                self.dpl_asset_parts = dpl_asset_parts
            else:
                self.dpl_asset_parts = '2'

            self.dpl_template = asset_timestamp + '_template_' + self.dpl_asset_parts
        else:
            self.dpl_asset_parts = ""
            self.dpl_template = ""



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
