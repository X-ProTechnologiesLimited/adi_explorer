from .models import MEDIA_LIBRARY, ADI_main, ADI_EST_Show, ADI_metadata, ADI_media, ADI_offer
from . import db
def delete_supp_file(filename):
    MEDIA_LIBRARY.query.filter_by(filename=filename).delete()
    db.session.commit()


def delete_asset_est_group(assetId):
    ADI_main.query.filter_by(assetId=assetId).delete()
    ADI_media.query.filter_by(assetId=assetId).delete()
    ADI_offer.query.filter_by(assetId=assetId).delete()
    ADI_metadata.query.filter_by(assetId=assetId).delete()
    ADI_EST_Show.query.filter_by(assetId=assetId).delete()
    db.session.commit()

def delete_asset_standard(assetId):
    ADI_main.query.filter_by(assetId=assetId).delete()
    ADI_media.query.filter_by(assetId=assetId).delete()
    ADI_offer.query.filter_by(assetId=assetId).delete()
    ADI_metadata.query.filter_by(assetId=assetId).delete()
    ADI_EST_Show.query.filter_by(assetId=assetId).delete()
    db.session.commit()


def delete_asset_est_episode(assetId):
    ADI_main.query.filter_by(assetId=assetId).delete()
    ADI_media.query.filter_by(assetId=assetId).delete()
    ADI_offer.query.filter_by(assetId=assetId).delete()
    ADI_metadata.query.filter_by(assetId=assetId).delete()
    ADI_EST_Show.query.filter_by(assetId=assetId).delete()
    db.session.commit()


