from . import movie_config
class adi_package_logic(object):

    def __init__(self):
        self.movie_path = None
        self.image_path = None
        self.asset_duration = None
        self.dpl_mid_rolls = None
        self.term_type = None

    def path_builder(self, asset_type):
        if 'VRP' in asset_type:
            self.image_path = ""
            self.movie_path = ""
        else:
            self.image_path = 'tank/' + movie_config.image_path
            self.movie_path = movie_config.video_path

    def duration_calc(self, runtime):
        self.asset_duration = 'PT' + runtime.split(':')[0] + 'H' + runtime.split(':')[1] + 'M' + runtime.split(':')[2] + 'S'

    def dpl_midroll_calc(self, asset_type, total_asset_parts):
        if 'DPL' not in asset_type:
            self.dpl_mid_rolls = ""
        else:
            self.dpl_mid_rolls = str(int(total_asset_parts) - 1)

    def term_type_generate(self, asset_type):
        if 'CATCHUP' in asset_type:
            self.term_type = 'CUTV'
        else:
            self.term_type = 'Archive'
