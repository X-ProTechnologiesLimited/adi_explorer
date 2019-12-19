from flask import Blueprint, jsonify, render_template
from os import path
from json2html import *

errorchecker = Blueprint('errorchecker', __name__)
basepath = path.dirname(__file__)
html_outfile = path.abspath(path.join(basepath, "..", "templates", "search_response.html"))

@errorchecker.errorhandler(501)
def internal_server_error():
    message = {
        'status' : 501,
        'message' : 'Did not create ADI successfully'
    }
    output = json2html.convert(json=message,
                               table_attributes="id=\"Error\" class=\"table table-striped\"" "border=2")
    with open(html_outfile, 'w') as outf:
        outf.write('{% extends "base.html" %}')
        outf.write('{% block content %}')
        outf.write(output)
        outf.write('{% endblock %}')

    return render_template('search_response.html')


@errorchecker.errorhandler(502)
def not_supported_asset_type(asset_type):
    message = {
            'status': 502,
            'message': 'Asset Type: ' + asset_type + ' is not supported yet'
        }
    output = json2html.convert(json=message,
                               table_attributes="id=\"Error\" class=\"table table-striped\"" "border=2")
    with open(html_outfile, 'w') as outf:
        outf.write('{% extends "base.html" %}')
        outf.write('{% block content %}')
        outf.write(output)
        outf.write('{% endblock %}')

    return render_template('search_response.html')


@errorchecker.errorhandler(502)
def not_implemented_yet():
    message = {
            'status': 502,
            'message': 'This requirement is not yet implemented'
        }
    output = json2html.convert(json=message,
                               table_attributes="id=\"Error\" class=\"table table-striped\"" "border=2")
    with open(html_outfile, 'w') as outf:
        outf.write('{% extends "base.html" %}')
        outf.write('{% block content %}')
        outf.write(output)
        outf.write('{% endblock %}')

    return render_template('search_response.html')


@errorchecker.errorhandler(502)
def not_supported_offer_count(offer_count):
    message = {
            'status': 502,
            'message': 'Offer_Count: ' + offer_count + ' is not supported yet'
        }
    output = json2html.convert(json=message,
                               table_attributes="id=\"Error\" class=\"table table-striped\"" "border=2")
    with open(html_outfile, 'w') as outf:
        outf.write('{% extends "base.html" %}')
        outf.write('{% block content %}')
        outf.write(output)
        outf.write('{% endblock %}')

    return render_template('search_response.html')

@errorchecker.errorhandler(404)
def not_matched_criteria():
    message = {
            'status': 404,
            'message': 'No Assets match this search criteria'
        }
    output = json2html.convert(json=message,
                               table_attributes="id=\"Error\" class=\"table table-striped\"" "border=2")
    with open(html_outfile, 'w') as outf:
        outf.write('{% extends "base.html" %}')
        outf.write('{% block content %}')
        outf.write(output)
        outf.write('{% endblock %}')

    return render_template('search_response.html')


@errorchecker.errorhandler(404)
def asset_not_found_id(assetId):
    message = {
            'status': 404,
            'message': 'No Assets are found with this AssetId: ' + assetId
        }
    output = json2html.convert(json=message,
                               table_attributes="id=\"Error\" class=\"table table-striped\"" "border=2")
    with open(html_outfile, 'w') as outf:
        outf.write('{% extends "base.html" %}')
        outf.write('{% block content %}')
        outf.write(output)
        outf.write('{% endblock %}')

    return render_template('search_response.html')

@errorchecker.errorhandler(404)
def no_assets_in_db():
    message = {
            'status': 404,
            'message': 'No Assets are found in the database'
        }
    output = json2html.convert(json=message,
                               table_attributes="id=\"Error\" class=\"table table-striped\"" "border=2")
    with open(html_outfile, 'w') as outf:
        outf.write('{% extends "base.html" %}')
        outf.write('{% block content %}')
        outf.write(output)
        outf.write('{% endblock %}')

    return render_template('search_response.html')


@errorchecker.errorhandler(404)
def undefined_update_field(update_field):
    message = {
            'status': 404,
            'message': 'Update ADI using this ' + update_field + ' is not yet implemented'
        }
    output = json2html.convert(json=message,
                               table_attributes="id=\"Error\" class=\"table table-striped\"" "border=2")
    with open(html_outfile, 'w') as outf:
        outf.write('{% extends "base.html" %}')
        outf.write('{% block content %}')
        outf.write(output)
        outf.write('{% endblock %}')

    return render_template('search_response.html')


@errorchecker.errorhandler(502)
def input_missing(input_field):
    message = {
            'status': 502,
            'message': 'input field: ' + input_field + ' missing for this request'
        }
    output = json2html.convert(json=message,
                               table_attributes="id=\"Error\" class=\"table table-striped\"" "border=2")
    with open(html_outfile, 'w') as outf:
        outf.write('{% extends "base.html" %}')
        outf.write('{% block content %}')
        outf.write(output)
        outf.write('{% endblock %}')

    return render_template('search_response.html')