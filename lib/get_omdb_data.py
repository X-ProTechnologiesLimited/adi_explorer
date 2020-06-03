# Filename: lib/get_omdb_data.py
"""
Created on June 01, 2020

@author: Krishnendu Banerjee
@summary: This file holds the function to retrieve Realistic data from Open Source Movie Database

"""

import requests, os
from PIL import Image # Python Native Image Processing Library
from resizeimage import resizeimage
from . import movie_config, response, errorchecker, create_tar, api_media_library
from bson.json_util import dumps
IMAGE_FETCH_DIRECTORY = movie_config.omdb_image_dir
IMAGE_UPLOAD_DIRECTORY = movie_config.premium_upload_dir+'/'

def get_omdb_data(omdb_title):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function to Retrieve Realistic Data from OMDB open API
    :access: public.
    :param omdb_title:
    :return: Response as JSON
    """
    omdb_host = movie_config.omdb_host
    api_key = movie_config.omdb_api_key
    omdb_url = omdb_host + omdb_title + '&apikey=' + api_key
    response_omdb = requests.get(url=omdb_url)
    try:
        response_omdb_json = response_omdb.json()
        omdb_map = {}
        omdb_map['packages'] = {}
        omdb_map['packages']['Title'] = response_omdb_json['Title']
        omdb_map['packages']['Synopsis'] = response_omdb_json['Plot']
        omdb_map['packages']['Image_URL'] = response_omdb_json['Poster']
        omdb_map['packages']['Year'] = response_omdb_json['Year'][0:4]
        image_url = response_omdb_json['Poster']
        myfile = requests.get(image_url)
        open(IMAGE_FETCH_DIRECTORY+'OMDB_base.jpg', 'wb').write(myfile.content)

        json_data = dumps(omdb_map)
        return response.asset_retrieve(json_data)

    except:
        return errorchecker.omdb_data_not_found(omdb_title)


def omdb_image_create(title):
    """
    :author: Krishnendu Banerjee.
    :date: 29/03/2020.
    :description: Creates the Purchase Options for EST Assets.
    :access: public
    :param title: Title of the Asset
    :return: List the Files Created
    """
    title = title.replace(' ', '')
    with open(IMAGE_FETCH_DIRECTORY+'OMDB_base.jpg', 'r+b') as f:
        with Image.open(f) as image:
            cover = resizeimage.resize_cover(image, [182, 98], validate=False)
            filename_182x98 = title+'_182x98.jpg'
            cover.save(IMAGE_UPLOAD_DIRECTORY+filename_182x98, image.format)
            checksum = api_media_library.checksum_creator(os.path.join(IMAGE_UPLOAD_DIRECTORY, filename_182x98))
            create_tar.add_supporting_files_to_db(filename_182x98, checksum, title)
            cover = resizeimage.resize_cover(image, [182, 243], validate=False)
            filename_182x243 = title + '_182x243.jpg'
            cover.save(IMAGE_UPLOAD_DIRECTORY + filename_182x243, image.format)
            checksum = api_media_library.checksum_creator(os.path.join(IMAGE_UPLOAD_DIRECTORY, filename_182x243))
            create_tar.add_supporting_files_to_db(filename_182x243, checksum, title)
            cover = resizeimage.resize_cover(image, [800, 600], validate=False)
            filename_800x600 = title + '_800x600.jpg'
            cover.save(IMAGE_UPLOAD_DIRECTORY + filename_800x600, image.format)
            checksum = api_media_library.checksum_creator(os.path.join(IMAGE_UPLOAD_DIRECTORY, filename_800x600))
            create_tar.add_supporting_files_to_db(filename_800x600, checksum, title)
            cover = resizeimage.resize_cover(image, [1920, 1080], validate=False)
            filename_1920x1080 = title + '_1920x1080.jpg'
            cover.save(IMAGE_UPLOAD_DIRECTORY + filename_1920x1080, image.format)
            checksum = api_media_library.checksum_creator(os.path.join(IMAGE_UPLOAD_DIRECTORY, filename_1920x1080))
            create_tar.add_supporting_files_to_db(filename_1920x1080, checksum, title)
            cover = resizeimage.resize_cover(image, [262, 349], validate=False)
            filename_262x349 = title + '_262x349.jpg'
            cover.save(IMAGE_UPLOAD_DIRECTORY + filename_262x349, image.format)
            checksum = api_media_library.checksum_creator(os.path.join(IMAGE_UPLOAD_DIRECTORY, filename_262x349))
            create_tar.add_supporting_files_to_db(filename_262x349, checksum, title)
            cover = resizeimage.resize_cover(image, [456, 257], validate=False)
            filename_456x257 = title + '_456x257.jpg'
            cover.save(IMAGE_UPLOAD_DIRECTORY + filename_456x257, image.format)
            checksum = api_media_library.checksum_creator(os.path.join(IMAGE_UPLOAD_DIRECTORY, filename_456x257))
            create_tar.add_supporting_files_to_db(filename_456x257, checksum, title)

    return api_media_library.list_files_checksum()
