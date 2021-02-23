# Filename: lib/response.py
"""
Created on June 01, 2020

@author: Krishnendu Banerjee
@summary: This file holds the functions to serialise all the different successful responses to a JSON format
"""

from flask import Blueprint, render_template
from os import path
from json2html import *
from w3lib.html import replace_entities

response = Blueprint('response', __name__)
basepath = path.dirname(__file__)
html_outfile = path.abspath(path.join(basepath, "..", "templates", "search_response.html"))


def response_creator(message):
    output = json2html.convert(json=message,
                               table_attributes="id=\"Error\" class=\"table table-striped\"" 
                                                "border=2")
    output_escaped = replace_entities(output)
    with open(html_outfile, 'w') as outf:
        outf.write('{% extends "base.html" %}')
        outf.write('{% block content %}')
        outf.write('<div class="container">')
        outf.write(output_escaped)
        outf.write('</div>')
        outf.write('{% endblock %}')

    return render_template('search_response.html')

def asset_retrieve(json_data):
    output = json2html.convert(json=json_data,
                               table_attributes="id=\"Error\" class=\"table table-striped\"" 
                                                "border=2")
    output_escaped = replace_entities(output)
    with open(html_outfile, 'w') as outf:
        outf.write('{% extends "base.html" %}')
        outf.write('{% block content %}')
        outf.write('<div class="container">')
        outf.write(output_escaped)
        outf.write('</div>')
        outf.write('{% endblock %}')

    return render_template('search_response.html')


def asset_retrieve_form(json_data):
    output = json2html.convert(json=json_data,
                               table_attributes="id=\"Error\" class=\"table table-striped\"" 
                                                "border=2")
    output_escaped = replace_entities(output)
    with open(html_outfile, 'w') as outf:
        outf.write('{% extends "base.html" %}')
        outf.write('{% block content %}')
        outf.write('<div class="container">')
        outf.write('<div class="sticky_2">')
        outf.write('<form method="POST" id="view" action="/adi">')
        outf.write('<input type="submit" name="form_view" class="button_view" value="View ADI"><br>')
        outf.write('<p>')
        outf.write(' <input type="submit" name="form_download" class="button_view" value="Download ADI"><br>')
        outf.write('<p>')
        outf.write(' <input type="submit" name="form_ingest" class="button_ingest" value="Ingest"><br>')
        outf.write('<p>')
        outf.write(' <input type="submit" name="form_ingest_history" class="button_ingest" value="Conversation"><br>')
        outf.write('<p>')
        outf.write(' <input type="submit" name="form_est_offers" class="button_meta" value="EST Offers"><br>')
        outf.write('<p>')
        outf.write(' <input type="submit" name="form_metadata" class="button_meta" value="Metadata"><br>')
        outf.write('<p>')
        outf.write(' <input type="submit" name="form_clone" class="button_assist" value="Clone"><br>')
        outf.write('<p>')
        outf.write(' <input type="submit" name="form_download_bs" class="button_assist" value="Download Show"><br>')
        outf.write('<p>')
        outf.write(' <input type="submit" name="form_update_meta" class="button_update" value="Update Meta"><br>')
        outf.write('<p>')
        outf.write(' <input type="submit" name="form_update_mov" class="button_update" value="Update Mov"><br>')
        outf.write('<p>')
        outf.write(' <input type="submit" name="form_update_prev" class="button_update" value="Update Prev"><br>')
        outf.write('<p>')
        outf.write('</div>')
        outf.write(output_escaped)
        outf.write('</form>')
        outf.write('</div>')
        outf.write('{% endblock %}')

    return render_template('search_response.html')


def asset_update_success(assetId, update_field):
    asset_encoded = '<a href="/get_adi/' + assetId + '">' + assetId + '</a>'
    message = {
            'status': 200,
            'message': update_field + ': updated successfully for asset with AssetId: ' + asset_encoded
        }
    return response_creator(message)

def asset_delete_success(assetId):
    message = {
            'status': 200,
            'message': 'Asset with AssetId: ' + assetId + ' deleted successfully'
        }
    return response_creator(message)



def asset_creation_success(assetId, title):
    asset_encoded = '<a href="/get_adi/' + assetId + '">' + assetId + '</a>'
    message = {
            'status': 200,
            'message': 'Asset: ' + title + ' created successfully with AssetId: ' + asset_encoded,
            'download': 'To download the asset ADI, use the View > Download ADI Menu OR click Above'
        }
    return response_creator(message)


def file_upload_successful(filename):
    message = {
            'status': 200,
            'message': 'Filename: ' + filename + ' uploaded successfully'
        }
    return response_creator(message)

def default_config_load_success(config_name, value):
    message = {
            'status': 200,
            'message': 'Default Config: ' + config_name + ' updated successfully to: ' + value
        }
    return response_creator(message)