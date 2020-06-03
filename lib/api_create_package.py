# lib/api_create_package.py
"""
Created on May 27, 2020

@author: Krishnendu Banerjee
@summary: This file is responsible for creating the Create Asset APIs:

"""
from flask import Blueprint, render_template, request
from .models import MEDIA_LIBRARY
from . import errorchecker, create_asset, create_tar, movie_config
from . import db

api_create_package = Blueprint('api_create_package', __name__)

@api_create_package.route('/create_single_title/<package>', methods=['GET', 'POST'])
def create_single_title(package):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that creates the Create Single Title API and calls create asset module
    :access: public.
    :method: get and post
    :param package: This input parameter states if Package is normal or VRP
    :return: get: render Jinja template templates/create_single_title.html
    :return: post: module: create_asset; function: create_single_title()
    """
    video_filename = 'ts'
    search = "%{}%".format(video_filename)
    library = MEDIA_LIBRARY.query.filter(MEDIA_LIBRARY.filename.like(search))
    image_group_name = db.session.query(MEDIA_LIBRARY.image_group).distinct().filter(MEDIA_LIBRARY.image_group != 'None')
    if request.method == 'POST':
        return create_asset.create_single_title()
    return render_template('create_single_title.html', library=library, image_group_name=image_group_name, package=package)


@api_create_package.route('/create_est/<package>', methods=['GET', 'POST'])
def create_est(package):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that creates the EST Packages API and calls create EST Module
    :access: public
    :method: get and post
    :param package: show or single_title; called by: templates/base.html action; mandatory
    :return: get: render Jinja template templates/create_box_set.html OR templates/create_est_title.html
    :return: post: module: create_asset; function: create_est_title_adi()
    """
    video_filename = 'ts'
    search = "%{}%".format(video_filename)
    library = MEDIA_LIBRARY.query.filter(MEDIA_LIBRARY.filename.like(search))
    image_group_name = db.session.query(MEDIA_LIBRARY.image_group).distinct().filter(MEDIA_LIBRARY.image_group != 'None')
    if package == 'show':
        if request.method == 'POST':
            return create_asset.create_est_show_adi()
        return render_template('create_box_set.html', library=library, image_group_name=image_group_name)
    elif package == 'single_title':
        if request.method == 'POST':
            return create_asset.create_est_title_adi()
        return render_template('create_est_title.html', library=library, image_group_name=image_group_name)
    else:
        return errorchecker.not_supported_asset_type(package)


@api_create_package.route("/create_tar", methods=['GET', 'POST'])
def make_tarfile():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that creates the VRP TAR File API and calls create Tar Module
    :access: public
    :form_input: filename: Filename of the VRP TAR File
    :method: get and post
    :return: get: render Jinja template templates/create_tar.html
    :return: post: module: create_tar; function: make_tarfile(filename)
    """
    filename = request.form.get('filename')
    if request.method == 'POST':
        return create_tar.make_tarfile(filename)
    return render_template('create_tar.html')

@api_create_package.route("/clone_adi", methods=['GET', 'POST'])
def clone_adi():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that creates the clone API and calls clone Asset module
    :access: public.
    :form_input: assetId: Asset Id for the asset that needs to be cloned
    :form_input: title: Specify the title of the Cloned Asset
    :method: get and post
    :return: get: Render Jinja template templates/clone_adi.html
    :return: post: module: create_asset; function: clone_asset
    """
    if request.method == 'POST':
        return create_asset.clone_asset()
    return render_template('clone_adi.html')
