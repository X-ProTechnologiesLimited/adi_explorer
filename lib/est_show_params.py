from . import movie_config
class est_show_default_params(object):

    def __init__(self):
        self.est_show_provider = None
        self.est_episode_provider = None
        self.est_episode_title = None
        self.no_of_seasons = None
        self.no_of_episodes = None

    def est_show_type_entry(self, show_type, title):
        if show_type == 'Movie BS':
            self.est_show_provider = movie_config.movie_show_provider
            self.est_episode_provider = movie_config.movie_episode_provider
            self.est_episode_title = title + ':Mov:'
        else:
            self.est_show_provider = movie_config.tv_show_provider
            self.est_episode_provider = movie_config.tv_episode_provider
            self.est_episode_title = title + ':Ep:'

    def est_series_count(self, no_of_seasons, no_of_episodes):
        if no_of_seasons == "":
            self.no_of_seasons = movie_config.default_no_of_seasons
        else:
            self.no_of_seasons = no_of_seasons
        if no_of_episodes == "":
            self.no_of_episodes = movie_config.default_no_of_episodes
        else:
            self.no_of_episodes = no_of_episodes