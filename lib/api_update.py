# lib/api_update.py
"""
Created on May 29, 2020

@author: Krishnendu Banerjee
@summary: This file is responsible for creating the Update Asset APIs

"""
from flask import Blueprint, render_template, request
from . import update_package

api_update= Blueprint('api_update', __name__)

@api_update.route('/update_single_title', methods=['GET', 'POST'])
def update_single_title():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that calls the Update Metadata APIs for the Assets
    :access: public
    :method: get and post
    :return: get: Return Jinja Template for templates/update_single_title.html
    :return: post: module: update_package; function: update_single_title
    """
    if request.method == 'POST':
        return update_package.update_single_title()
    return render_template('update_single_title.html')


@api_update.route('/update_video/<movie_type>', methods=['GET', 'POST'])
def update_video(movie_type):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that calls the Update Video File and Trailer APIs for assets
    :access: public
    :method: get and post
    :param movie_type: main video or trailer, called by templates/base.html
    :return: get: return Jinja template for templates/update_video.html
    :return: post: module: update_package; function: update_asset_video(movie_type)
    """
    if request.method == 'POST':
        return update_package.update_asset_video(movie_type)
    return render_template('update_video.html', movie_type=movie_type)