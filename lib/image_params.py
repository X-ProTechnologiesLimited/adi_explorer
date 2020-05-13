from flask import request
from .models import MEDIA_LIBRARY, MEDIA_DEFAULT
class image_default_params(object):

    def __init__(self):
        self.asset_image = {}

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
            self.asset_image['image_1'] = file_pref + '_THUM.jpg'
            self.asset_image['image_2']  = file_pref + '_CATI.jpg'
            self.asset_image['image_3']  = file_pref + '_PRAW.jpg'
            self.asset_image['image_4']  = file_pref + '_PRIW.jpg'
            self.asset_image['image_5']  = file_pref + '_PRSW.jpg'
            self.asset_image['image_6']  = file_pref + '_PRMW.jpg'
            self.asset_image['image_1_checksum'] = self.get_checksum(self.asset_image['image_1'])
            self.asset_image['image_2_checksum'] = self.get_checksum(self.asset_image['image_2'])
            self.asset_image['image_3_checksum'] = self.get_checksum(self.asset_image['image_3'])
            self.asset_image['image_4_checksum'] = self.get_checksum(self.asset_image['image_4'])
            self.asset_image['image_5_checksum'] = self.get_checksum(self.asset_image['image_5'])
            self.asset_image['image_6_checksum'] = self.get_checksum(self.asset_image['image_6'])
        else:
            if request.form.get('image_group') == "":
                file_pref = image_path_default.standard_image_file_prefix
            else:
                file_pref = request.form.get('image_group')
            self.asset_image['image_1'] = file_pref + '_182x98.jpg'
            self.asset_image['image_2'] = file_pref + '_182x243.jpg'
            self.asset_image['image_3'] = file_pref + '_262x349.jpg'
            self.asset_image['image_4'] = file_pref + '_456x257.jpg'
            self.asset_image['image_5'] = ""
            self.asset_image['image_6'] = ""
            self.asset_image['image_1_checksum'] = self.get_checksum(self.asset_image['image_1'])
            self.asset_image['image_2_checksum'] = self.get_checksum(self.asset_image['image_2'])
            self.asset_image['image_3_checksum'] = self.get_checksum(self.asset_image['image_3'])
            self.asset_image['image_4_checksum'] = self.get_checksum(self.asset_image['image_4'])
            self.asset_image['image_5_checksum'] = ""
            self.asset_image['image_6_checksum'] = ""