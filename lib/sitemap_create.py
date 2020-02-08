from . import movie_config
from . import errorchecker
class sitemap_mapper(object):

    def __init__(self):
        self.sitemap = None

    def sitemap_entry(self, asset_type):
        if 'DPL' not in asset_type:
            self.sitemap = 'ASSET_STANDARD_TITLE.xml'
        elif 'DPL' in asset_type:
            self.sitemap = 'ASSET_DPL_TITLE.xml'
        else:
            self.sitemap = False


    def sitemap_entry_boxset(self, asset_type, show_type):
        if asset_type == 'est_show':
            self.sitemap = 'ASSET_EST_SHOW.xml'
        elif asset_type == 'est_season':
            self.sitemap = 'ASSET_EST_SEASON.xml'
        elif asset_type == 'est_episode':
            if show_type == 'Movie BS':
                self.sitemap = 'ASSET_EST_MOVIE_EPISODE.xml'
            else:
                self.sitemap = 'ASSET_EST_EPISODE.xml'
        else:
            self.sitemap = False