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
        outf.write(output)
        outf.write('{% endblock %}')

    return render_template('search_response.html')

def asset_retrieve(json_data):
    output = json2html.convert(json=json_data,
                               table_attributes="id=\"Error\" class=\"table table-striped\"" "border=2")
    with open(html_outfile, 'w') as outf:
        outf.write('{% extends "base.html" %}')
        outf.write('{% block content %}')
        outf.write(output)
        outf.write('{% endblock %}')

    return render_template('search_response.html')


def asset_update_success(assetId, update_field):
    message = {
            'status': 200,
            'message': update_field + ' of Asset with assetId: ' + assetId + ' updated successfully'
        }
    output = json2html.convert(json=message,
                               table_attributes="id=\"Error\" class=\"table table-striped\"" "border=2")
    return response_creator(message)



def asset_creation_success(assetId, title):
    message = {
            'status': 200,
            'message': 'Asset with AssetId: ' + assetId + ' and Title: ' + title + ' created successfully',
            'download': 'To download the asset ADI, use the Download Menu'
        }
    return response_creator(message)