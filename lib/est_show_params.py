from . import movie_config, offerdate
class est_show_default_params(object):

    def __init__(self):
        self.est_show_provider = None
        self.est_episode_provider = None
        self.est_episode_title = None
        self.no_of_seasons = None
        self.no_of_episodes = None
        self.po_offer_window = None
        self.cs_offer_window = None
        self.reg_offer_window = None
        self.po_start = None
        self.po_end = None
        self.cs_start = None
        self.cs_end = None
        self.reg_start = None
        self.reg_end = None


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

    def est_offer_window_entry(self, po_offer_window, cs_offer_window, reg_offer_window):
        if po_offer_window != "":
            self.po_offer_window = po_offer_window
        else:
            self.po_offer_window = '7'

        if cs_offer_window != "":
            self.cs_offer_window = cs_offer_window
        else:
            self.cs_offer_window = '7'

        if reg_offer_window != "":
            self.reg_offer_window = reg_offer_window
        else:
            self.reg_offer_window = '30'

    def est_offer_date_entry(self, order_type, po_offer_window, cs_offer_window, reg_offer_window):
        if order_type == "PO":
            self.po_start = offerdate.offer_date(0, 0)
            self.po_end = offerdate.offer_date(int(po_offer_window), 0)
        elif order_type == "PO+CS":
            po_cs_window = int(po_offer_window) + int(cs_offer_window)
            self.po_start = offerdate.offer_date(0, 0)
            self.po_end = offerdate.offer_date(int(po_offer_window), 0)
            self.cs_start = offerdate.offer_date(int(po_offer_window), 1)
            self.cs_end = offerdate.offer_date(po_cs_window, 0)
        elif order_type == "REG":
            self.reg_start = offerdate.offer_date(0, 0)
            self.reg_end = offerdate.offer_date(int(reg_offer_window), 0)
        elif order_type == "PO+CS+REG":
            po_cs_window = int(po_offer_window) + int(cs_offer_window)
            po_cs_reg_window = int(po_offer_window) + int(cs_offer_window) + int(reg_offer_window)
            self.po_start = offerdate.offer_date(0, 0)
            self.po_end = offerdate.offer_date(int(po_offer_window), 0)
            self.cs_start = offerdate.offer_date(int(po_offer_window), 1)
            self.cs_end = offerdate.offer_date(po_cs_window, 0)
            self.reg_start = offerdate.offer_date(po_cs_window, 1)
            self.reg_end = offerdate.offer_date(po_cs_reg_window, 0)





