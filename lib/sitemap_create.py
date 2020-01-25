class sitemap_mapper(object):

    def __init__(self):
        self.sitemap = None

    def sitemap_entry(self, asset_type, subtitle_flag):
        if 'DPL' not in asset_type and (('VOD' in asset_type) or ('RENTAL' in asset_type)) and subtitle_flag == 'true':
            self.sitemap = 'VOD_SINGLE_TITLE.xml'
        elif 'DPL' not in asset_type and (('VOD' in asset_type) or ('RENTAL' in asset_type)) and subtitle_flag == 'false':
            self.sitemap = 'VOD_SINGLE_TITLE_NOSUB.xml'
        elif asset_type == 'EST SINGLE TITLE':
            self.sitemap = 'EST_SINGLE_TITLE.xml'
        elif 'CATCHUP' in asset_type:
            self.sitemap = 'CUTV.xml'
        elif (asset_type == 'SUBSCRIPTION EPISODE') or (asset_type == 'VRP SUBSCRIPTION EPISODE'):
            self.sitemap = 'SVOD_E.xml'
        elif 'DPL SUBSCRIPTION VOD' in asset_type:
            self.sitemap = 'DPL_VOD.xml'
        elif 'DPL CATCHUP' in asset_type:
            self.sitemap = 'DPL_CUTV.xml'
        elif 'DPL SUBSCRIPTION EPISODE' in asset_type:
            self.sitemap = 'DPL_SVOD_E.xml'
        elif (asset_type == 'est_show') or (asset_type == 'est_season') or (asset_type == 'est_episode'):
            self.sitemap = True
        else:
            self.sitemap = False


    def sitemap_entry_boxset(self, asset_type, show_type):
        if asset_type == 'est_show':
            self.sitemap = 'EST_SHOW.xml'
        elif asset_type == 'est_season':
            self.sitemap = 'EST_SEASON.xml'
        elif asset_type == 'est_episode':
            if show_type == 'Movie BS':
                self.sitemap = 'EST_MOVIE_EPISODE.xml'
            else:
                self.sitemap = 'EST_EPISODE.xml'
        else:
            self.sitemap = False