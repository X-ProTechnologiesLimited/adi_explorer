import requests
from . import movie_config, response, errorchecker
from bson.json_util import dumps

def get_omdb_data(omdb_title):
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

        json_data = dumps(omdb_map)
        return response.asset_retrieve(json_data)
    except:
        return errorchecker.omdb_data_not_found(omdb_title)
