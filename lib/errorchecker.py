# Filename: lib/errorchecker.py
"""
Created on June 01, 2020

@author: Krishnendu Banerjee
@summary: This file holds the function to handle all the error messages for the tool

"""

from flask import Blueprint, render_template
from os import path
from json2html import *

errorchecker = Blueprint('errorchecker', __name__)
basepath = path.dirname(__file__)
html_outfile = path.abspath(path.join(basepath, "..", "templates", "search_response.html"))

def error_response_creator(message):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function to delete the EST Group Assets
    :access: public.
    :param message: This is the error message
    :return: render Jinja template templates/searh_response.html
    """
    output = json2html.convert(json=message,
                               table_attributes="id=\"Error\" class=\"table table-striped\"" "border=2")
    with open(html_outfile, 'w') as outf:
        outf.write('{% extends "base.html" %}')
        outf.write('{% block content %}')
        outf.write('<div class="container">')
        outf.write(output)
        outf.write('</div>')
        outf.write('{% endblock %}')

    return render_template('search_response.html')

@errorchecker.errorhandler(501)
def internal_server_error():
    message = {
        'status': 501,
        'message': 'Internal Server Error. Could not update database.'
    }
    return error_response_creator(message)


@errorchecker.errorhandler(501)
def file_already_uploaded(filename):
    message = {
        'status': 501,
        'message': 'This supporting file: ' + filename + ' is already added to the library.',
        'view': 'To view the supporting files, please use option VRP management > Show VRP Library'
    }
    return error_response_creator(message)



@errorchecker.errorhandler(501)
def internal_server_error_show(show_type):
    message = {
        'status': 501,
        'message': 'Not able to create the Package for ' + show_type
    }
    return error_response_creator(message)

@errorchecker.errorhandler(502)
def not_supported_asset_type(asset_type):
    message = {
            'status': 502,
            'message': 'Asset Type: ' + asset_type + ' is not supported for this operation'
        }
    return error_response_creator(message)


@errorchecker.errorhandler(502)
def vrp_asset_type(asset_type):
    message = {
            'status': 502,
            'message': 'Asset Type: ' + asset_type + ' should be created from VRP or DPL menu. Please refer User Guide.'
        }
    return error_response_creator(message)



@errorchecker.errorhandler(502)
def use_different_method(asset_type):
    message = {
            'status': 502,
            'message': 'Use the Other Download Package option for asset type: ' + asset_type
        }
    return error_response_creator(message)

@errorchecker.errorhandler(502)
def not_implemented_yet():
    message = {
            'status': 502,
            'message': 'This requirement is not yet implemented'
        }
    return error_response_creator(message)

@errorchecker.errorhandler(502)
def not_supported_offer_count(offer_count):
    message = {
            'status': 502,
            'message': 'Offer_Count: ' + offer_count + ' is not supported yet'
        }
    return error_response_creator(message)

@errorchecker.errorhandler(404)
def not_matched_criteria():
    message = {
            'status': 404,
            'message': 'No Assets match this search criteria'
        }
    return error_response_creator(message)


@errorchecker.errorhandler(404)
def asset_not_found_id(assetId):
    message = {
            'status': 404,
            'message': 'No Assets are found with this AssetId: ' + assetId
        }
    return error_response_creator(message)

@errorchecker.errorhandler(404)
def no_assets_in_db():
    message = {
            'status': 404,
            'message': 'No Assets are found in the database'
        }
    return error_response_creator(message)


@errorchecker.errorhandler(404)
def no_files_in_library():
    message = {
            'status': 404,
            'message': 'No Supporting Files are found in Library'
        }
    return error_response_creator(message)

@errorchecker.errorhandler(404)
def no_supporting_file(filename):
    message = {
            'status': 404,
            'message': 'Filename: ' + filename + ' is not available in Library'
        }
    return error_response_creator(message)


@errorchecker.errorhandler(404)
def undefined_update_field(update_field):
    message = {
            'status': 404,
            'message': 'Update ADI using this ' + update_field + ' is not yet implemented'
        }
    return error_response_creator(message)


@errorchecker.errorhandler(502)
def input_missing(input_field):
    message = {
            'status': 502,
            'message': 'input field: ' + input_field + ' missing for this request'
        }
    return error_response_creator(message)


@errorchecker.errorhandler(502)
def environment_not_defined(environment):
    message = {
            'status': 502,
            'message': 'Test Environment ' + environment + ' Not Defined or not valid'
        }
    return error_response_creator(message)

@errorchecker.errorhandler(502)
def missing_file_libary(filename):
    message = {
            'status': 502,
            'message': 'Filename ' + filename + ' seems to be missing in the library',
            'add_file': 'To add files to the library, use the VRP Management > Upload option first'
        }
    return error_response_creator(message)


@errorchecker.errorhandler(404)
def no_ingest_history(assetId):
    message = {
            'status': 404,
            'message': 'No Ingest History Found for this asset' + assetId
        }
    return error_response_creator(message)


@errorchecker.errorhandler(404)
def not_est_offer(assetId):
    message = {
            'status': 404,
            'message': 'Asset: ' + assetId + ' has no EST Offers Associated with it'
        }
    return error_response_creator(message)

@errorchecker.errorhandler(404)
def omdb_data_not_found(title):
    message = {
            'status': 404,
            'message': 'No OMDB Data found for this title: ' + title
        }
    return error_response_creator(message)


@errorchecker.errorhandler(502)
def upload_authentication_error():
    message = {
            'status': 502,
            'message': 'Upload Not Successful. Authentication error!'
        }
    return error_response_creator(message)

@errorchecker.errorhandler(404)
def upload_filenotfound_error(filename):
    message = {
            'status': 404,
            'message': 'Upload Not Successful. File: ' + filename + ' Not Found!'
        }
    return error_response_creator(message)