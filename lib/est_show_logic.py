class est_logic_entry(object):

    def __init__(self):
        self.est_show_provider = None
        self.est_episode_provider = None
        self.est_episode_title = None
        self.no_of_seasons = None
        self.no_of_episodes = None

    def est_show_type_entry(self, show_type, title):
        if show_type == 'Movie BS':
            self.est_show_provider = 'est__movieboxset_hd'
            self.est_episode_provider = 'est__moviebstitle_hd'
            self.est_episode_title = title + ': Movie: '
        else:
            self.est_show_provider = 'est__tvboxset_hd'
            self.est_episode_provider = 'est__tvepisode_hd'
            self.est_episode_title = title + ': Episode: '

    def est_series_count(self, no_of_seasons, no_of_episodes):
        if no_of_seasons == "":
            self.no_of_seasons = '1'
        else:
            self.no_of_seasons = no_of_seasons
        if no_of_episodes == "":
            self.no_of_episodes = '1'
        else:
            self.no_of_episodes = no_of_episodes