# Filename: lib/create_tar.py
"""
Created on June 01, 2020

@author: Krishnendu Banerjee
@summary: This file holds the function to create the VRP Tar Packages from Assets created in the Tool

"""

import requests, shutil, os, subprocess
from flask import request, send_from_directory
from . import movie_config, db, errorchecker, api_view
from .models import ADI_main, MEDIA_LIBRARY, ADI_media, ADI_EST_Show, ADI_metadata
from sqlalchemy.exc import IntegrityError

UPLOAD_DIRECTORY = movie_config.premium_upload_dir
VRP_PACKAGE_DIR = movie_config.premium_vrp_dir

def get_adi_xml(assetId, xml_file):
    """
    :author: Krishnendu Banerjee.
    :date: 29/03/2020.
    :description: Function to Save an ADI into a specified XML file.
    :access: public
    :param assetId: mandatory: Asset ID suppiled by the call
    :param xml_file: Filename to save thw XML into
    :return: XML File
    """
    my_filename = movie_config.adi_xml_dir + '/' + xml_file
    get_adi_url = 'http://localhost:5000/get_adi/' + assetId
    response_adi = requests.get(url=get_adi_url)
    with open(my_filename, 'w') as f:
        f.write(response_adi.text)


def make_tarfile(filename):
    """
    author: Krishnendu Banerjee.
    :date: 29/03/2020.
    :description: Function to create the VRP Tar File from an ADI adding the correct Media
    :access: public
    :param filename:
    :return: module: api_view; function: list_tar_files
    """
    output_filename = filename
    assetId = request.form.get('assetId')
    package_media = ADI_media.query.filter_by(assetId=assetId).first()
    package = ADI_main.query.filter_by(assetId=assetId).first()
    tar_filename = VRP_PACKAGE_DIR + '/' + output_filename
    if 'VRP' not in package.adi_type:
        return errorchecker.use_different_method(package.adi_type)

    my_filename = movie_config.premium_upload_dir + '/ADI.xml'
    get_adi_url = 'http://localhost:5000/get_adi/' + assetId
    response_adi = requests.get(url=get_adi_url)
    with open(my_filename, 'w') as f:
        f.write(response_adi.text)

    if 'VRP DPL' in package.adi_type:
        media_map = [package_media.movie_url, package_media.trailer_url, package_media.image_url_1,
                     package_media.image_url_2, package_media.image_url_3, package_media.image_url_4,
                     package_media.image_url_5, package_media.image_url_6]
        subprocess.call(['tar', '-C', UPLOAD_DIRECTORY, '-cf', tar_filename, media_map[0], media_map[1], media_map[2],
                         media_map[3], media_map[4], media_map[5], media_map[6], media_map[7], 'ADI.xml'])
    else:
        media_map = [package_media.movie_url, package_media.trailer_url, package_media.image_url_1,
                     package_media.image_url_2, package_media.image_url_3, package_media.image_url_4]
        subprocess.call(['tar', '-C', UPLOAD_DIRECTORY, '-cf', tar_filename, media_map[0], media_map[1], media_map[2],
                         media_map[3], media_map[4], media_map[5], 'ADI.xml'])

    return api_view.list_tar_files()


def add_supporting_files_to_db(filename, checksum, group):
    """
    :author: Krishnendu Banerjee.
    :date: 29/03/2020.
    :description: Creates the Purchase Options for EST Assets.
    :access: public
    :param filename: (Filename to be saved in the DB)
    :param checksum: (md5 checksum of the file)
    :param group: (This is the image group - needed to classify all images of a specific title together)
    :return: commit db session
    """
    new_filename = MEDIA_LIBRARY(filename=filename, checksum=checksum, image_group=group)
    db.session.add(new_filename)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return errorchecker.file_already_uploaded(filename)


def create_est_show_zip(show_asset_id):
    """
    :author: Krishnendu Banerjee.
    :date: 29/03/2020.
    :description: Function to Create a Zip File for all the related ADIS for an EST Show and download.
    :access: public
    :param show_asset_id: specify the assetId of the Main Show
    :return: Download ZIP file with all ADIs fot the EST show
    """
    get_adi_xml(show_asset_id, 'Show.xml')
    show_data = ADI_metadata.query.filter(ADI_metadata.assetId == show_asset_id).first()
    show_title = ''.join(show_data.title.split())
    for season in ADI_EST_Show.query.filter(ADI_EST_Show.parent_group_id == show_asset_id).all():
        get_adi_xml(season.assetId, 'Season' + season.season_number + '.xml')
        for episodes in ADI_EST_Show.query.filter(ADI_EST_Show.parent_group_id == season.assetId).all():
            get_adi_xml(episodes.assetId, 'S' + season.season_number + 'Ep' + episodes.episode_number + '.xml')

    shutil.make_archive(movie_config.premium_vrp_dir + '/Show_' + show_title, 'zip', movie_config.adi_xml_dir)
    adi_files = [f for f in os.listdir(movie_config.adi_xml_dir) if f.endswith('xml')]
    for item in adi_files:
        os.remove(os.path.join(movie_config.adi_xml_dir, item))
    return send_from_directory(VRP_PACKAGE_DIR, 'Show_' + show_title + '.zip', as_attachment=True)


