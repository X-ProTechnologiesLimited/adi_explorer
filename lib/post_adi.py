import requests
import datetime
import time
from .metadata_params import metadata_default_params
from . import get_asset_details
from . import errorchecker
from .models import ADI_main
params = metadata_default_params()

def post_adi_endpoint(assetId, environment, source):
    ts = time.time()
    conversationId = datetime.datetime.fromtimestamp(ts).strftime('%d%H%M%S')
    params.environment_entry(environment)
    try:
        package = ADI_main.query.filter_by(assetId=assetId).first()
        if package.adi_type == 'est_episode':
            request_adi = get_asset_details.download_est_episode(assetId)
        elif package.adi_type == 'est_season':
            request_adi = get_asset_details.download_est_season(assetId)
        elif package.adi_type == 'est_show':
            request_adi = get_asset_details.download_est_show(assetId)
        else:
            request_adi = get_asset_details.download_title(assetId)

        endpoint_url = params.environment_url + 'source=' + source + '&conversationId=' + conversationId
        headers = {'Content-type': 'text/xml;charset=\"utf-8\"'}
        response_adi_post = requests.post(url=endpoint_url, data=request_adi, headers=headers)
        return response_adi_post

    except:
        return errorchecker.asset_not_found_id(assetId)





