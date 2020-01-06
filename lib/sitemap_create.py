class sitemap_mapper(object):

    def __init__(self):
        self.sitemap = None

    def sitemap_entry(self, asset_type, subtitle_flag):
        if subtitle_flag == 'true':
            if (asset_type == 'PREMIUM VOD') or (asset_type == 'SUBSCRIPTION VOD') or (asset_type == 'RENTAL'):
                self.sitemap = 'VOD_SINGLE_TITLE.xml'
            elif (asset_type == 'EST SINGLE TITLE'):
                self.sitemap = 'EST_SINGLE_TITLE.xml'
            elif (asset_type == 'CATCHUP'):
                self.sitemap = 'CUTV.xml'
            else:
                self.sitemap = False
        elif subtitle_flag == 'false':
            if (asset_type == 'PREMIUM VOD') or (asset_type == 'SUBSCRIPTION VOD') or (asset_type == 'RENTAL'):
                self.sitemap = 'VOD_SINGLE_TITLE_NOSUB.xml'
            elif (asset_type == 'EST SINGLE TITLE'):
                self.sitemap = 'EST_SINGLE_TITLE.xml'
            elif (asset_type == 'CATCHUP'):
                self.sitemap = 'CUTV.xml'
            else:
                self.sitemap = False
        elif (asset_type == 'est_show') or (asset_type == 'est_season') or (asset_type == 'est_episode'):
            self.sitemap = True
        else:
            self.sitemap = False


    def sitemap_entry_boxset(self, asset_type):
        if (asset_type == 'est_show'):
            self.sitemap = 'EST_SHOW.xml'
        elif (asset_type == 'est_season'):
            self.sitemap = 'EST_SEASON.xml'
        elif (asset_type == 'est_episode'):
            self.sitemap = 'EST_EPISODE.xml'
        else:
            self.sitemap = False