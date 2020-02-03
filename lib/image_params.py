from . import movie_config
from . import errorchecker
from .models import MEDIA_LIBRARY, MEDIA_DEFAULT
class image_default_params(object):

    def __init__(self):
        self.image_1 = None
        self.image_1_checksum = None
        self.image_2 = None
        self.image_2_checksum = None
        self.image_3 = None
        self.image_3_checksum = None
        self.image_4 = None
        self.image_4_checksum = None
        self.image_5 = None
        self.image_5_checksum = None
        self.image_6 = None
        self.image_6_checksum = None

    def get_checksum(self, filename):
        file = MEDIA_LIBRARY.query.filter_by(filename=filename).first()
        return file.checksum

    def image_entry(self, asset_type):
        image_path_default = MEDIA_DEFAULT.query.first()
        if 'DPL' in asset_type:
            file_pref = image_path_default.dpl_image_file_prefix
            self.image_1 = file_pref + 'THUM.jpg'
            self.image_2 = file_pref + 'CATI.jpg'
            self.image_3 = file_pref + 'PRAW.jpg'
            self.image_4 = file_pref + 'PRIW.jpg'
            self.image_5 = file_pref + 'PRSW.jpg'
            self.image_6 = file_pref + 'PRMW.jpg'
            self.image_1_checksum = self.get_checksum(self.image_1)
            self.image_2_checksum = self.get_checksum(self.image_2)
            self.image_3_checksum = self.get_checksum(self.image_3)
            self.image_4_checksum = self.get_checksum(self.image_4)
            self.image_5_checksum = self.get_checksum(self.image_5)
            self.image_6_checksum = self.get_checksum(self.image_6)
        else:
            file_pref = image_path_default.standard_image_file_prefix
            self.image_1 = file_pref + '182x98.jpg'
            self.image_2 = file_pref + '182x243.jpg'
            self.image_3 = file_pref + '262x349.jpg'
            self.image_4 = file_pref + '456x257.jpg'
            self.image_5 = ""
            self.image_6 = ""
            self.image_1_checksum = self.get_checksum(self.image_1)
            self.image_2_checksum = self.get_checksum(self.image_2)
            self.image_3_checksum = self.get_checksum(self.image_3)
            self.image_4_checksum = self.get_checksum(self.image_4)
            self.image_5_checksum = ""
            self.image_6_checksum = ""
