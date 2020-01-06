from . import movie_config
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

    def param_logic_entry(self, synopsis, title, provider_version, production_year, ca_btc, par_rating, audio_type, frame_rate, subtitle_flag):
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


    def multiformat_entry(self, multiformat_id, asset_timestamp):
        if multiformat_id != "":
            self.multiformat_id = multiformat_id
        else:
            self.multiformat_id = 'BSKYPR' + asset_timestamp

    def movie_details_entry(self, provider_id):
        if 'hdr' in provider_id:
            self.movie_url = movie_config.hdr_movie_file
            self.movie_checksum = movie_config.hdr_movie_checksum
        elif '4k' in provider_id:
            self.movie_url = movie_config.sdr_movie_file
            self.movie_checksum = movie_config.sdr_movie_checksum
        elif 'est' in provider_id:
            self.movie_url = movie_config.est_movie_file
            self.movie_checksum = movie_config.est_movie_checksum
        elif ('hd.' in provider_id) or ('_hd' in provider_id):
            self.movie_url = movie_config.hd_movie_file
            self.movie_checksum = movie_config.hd_movie_checksum
        else:
            self.movie_url = movie_config.title_movie
            self.movie_checksum = movie_config.title_checksum

    def video_type_entry(self, provider_id):
        if ('hdr' in provider_id) or ('4k' in provider_id) or ('hd.' in provider_id) or ('_hd' in provider_id):
            self.video_type = 'true'
        else:
            self.video_type = 'false'

    def offer_type_entry(self, asset_type):
        if asset_type == 'SUBSCRIPTION VOD':
            self.offer_type = 'SVOD'
        else:
            self.offer_type = 'IPPR'