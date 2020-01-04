from . import movie_config
class parameter_logic(object):

    def __init__(self):
        self.synopsis = None
        self.provider_version = None
        self.production_year = None
        self.ca_btc = None
        self.par_rating = None
        self.audio_type = None
        self.frame_rate = None
        self.subtitle_flag = None

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

