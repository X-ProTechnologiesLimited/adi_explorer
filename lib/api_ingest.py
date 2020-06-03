# lib/api_ingest.py
"""
Created on May 27, 2020

@author: Krishnendu Banerjee
@summary: This file is responsible for creating the Ingest APIs:

"""

from flask import Blueprint, render_template, request
from .nocache import nocache
from . import search, get_asset_details


api_ingest = Blueprint('api_ingest', __name__)

@api_ingest.route('/post_adi', methods=['GET', 'POST'])
@nocache
def post_adi():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that creates the Post ADI API to endpoint
    :access: public.
    :method: get and post
    :return: get: Render Jinja template templates/post_adi.html
    :return: post: module: get_asset_details; function: post_adi_endpoint
    """
    if request.method == 'POST':
        return get_asset_details.post_adi_endpoint()
    return render_template('post_adi.html')

@api_ingest.route("/get_ingest_history", methods=['GET', 'POST'])
def get_ingest_history():
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function that creates the API to retrieve ingest history to specific environment
    :access: public.
    :method: get and post
    :return: get: Render Jinja template templates/asset_info.html; html_title=Get Ingest History, html_action=get_ingest_history
    :return: post: module: search; function: search_ingest_history
    """
    assetId = request.form.get('AssetId')
    if request.method == 'POST':
        return search.search_ingest_history(assetId)
    return render_template('asset_info.html', title='Get Ingest History', action='/get_ingest_history')