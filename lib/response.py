from flask import Blueprint, render_template
from os import path
from json2html import *

response = Blueprint('response', __name__)
basepath = path.dirname(__file__)
html_outfile = path.abspath(path.join(basepath, "..", "templates", "search_response.html"))


def response_creator(message):
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

def asset_retrieve(json_data):
    output = json2html.convert(json=json_data,
                               table_attributes="id=\"Error\" class=\"table table-striped\"" "border=2")
    with open(html_outfile, 'w') as outf:
        outf.write('{% extends "base.html" %}')
        outf.write('{% block content %}')
        outf.write('<div class="container">')
        outf.write(output)
        outf.write('</div>')
        outf.write('{% endblock %}')

    return render_template('search_response.html')


def asset_update_success(assetId, update_field):
    message = {
            'status': 200,
            'message': update_field + ': updated successfully for asset with AssetId: ' + assetId
        }
    return response_creator(message)

def asset_delete_success(assetId):
    message = {
            'status': 200,
            'message': 'Asset with AssetId: ' + assetId + ' deleted successfully'
        }
    return response_creator(message)



def asset_creation_success(assetId, title):
    message = {
            'status': 200,
            'message': 'Asset: ' + title + ' created successfully with AssetId: ' + assetId,
            'download': 'To download the asset ADI, use the View > Download ADI Menu'
        }
    return response_creator(message)


def file_upload_successful(filename, environment):
    message = {
            'status': 200,
            'message': 'Filename: ' + filename + ' uploaded successfully to ' + environment + ' location of tank'
        }
    return response_creator(message)

def default_config_load_success(config_name, value):
    message = {
            'status': 200,
            'message': 'Default Config: ' + config_name + ' updated successfully to: ' + value
        }
    return response_creator(message)