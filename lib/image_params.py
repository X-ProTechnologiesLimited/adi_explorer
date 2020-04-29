from flask import request
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
            if request.form.get('image_group') == "":
                file_pref = image_path_default.dpl_image_file_prefix
            else:
                file_pref = request.form.get('image_group')
            self.image_1 = file_pref + '_THUM.jpg'
            self.image_2 = file_pref + '_CATI.jpg'
            self.image_3 = file_pref + '_PRAW.jpg'
            self.image_4 = file_pref + '_PRIW.jpg'
            self.image_5 = file_pref + '_PRSW.jpg'
            self.image_6 = file_pref + '_PRMW.jpg'
            self.image_1_checksum = self.get_checksum(self.image_1)
            self.image_2_checksum = self.get_checksum(self.image_2)
            self.image_3_checksum = self.get_checksum(self.image_3)
            self.image_4_checksum = self.get_checksum(self.image_4)
            self.image_5_checksum = self.get_checksum(self.image_5)
            self.image_6_checksum = self.get_checksum(self.image_6)
        else:
            if request.form.get('image_group') == "":
                file_pref = image_path_default.standard_image_file_prefix
            else:
                file_pref = request.form.get('image_group')
            self.image_1 = file_pref + '_182x98.jpg'
            self.image_2 = file_pref + '_182x243.jpg'
            self.image_3 = file_pref + '_262x349.jpg'
            self.image_4 = file_pref + '_456x257.jpg'
            self.image_5 = ""
            self.image_6 = ""
            self.image_1_checksum = self.get_checksum(self.image_1)
            self.image_2_checksum = self.get_checksum(self.image_2)
            self.image_3_checksum = self.get_checksum(self.image_3)
            self.image_4_checksum = self.get_checksum(self.image_4)
            self.image_5_checksum = ""
            self.image_6_checksum = ""
