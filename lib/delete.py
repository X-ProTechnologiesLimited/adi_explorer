# Filename: lib/delete.py
"""
Created on June 01, 2020

@author: Krishnendu Banerjee
@summary: This file holds the function for Deleting Entries in the SQLite Database

"""
from .models import MEDIA_LIBRARY, ADI_main, ADI_EST_Show, ADI_metadata, ADI_media, ADI_offer, EST_PO
from . import db
def delete_supp_file(filename):
    MEDIA_LIBRARY.query.filter_by(filename=filename).delete()
    db.session.commit()


def delete_asset_est_group(assetId):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function to delete the EST Group Assets
    :access: public.
    :param assetId: This is the show Asset ID
    :return: commit delete transaction
    """
    ADI_main.query.filter_by(assetId=assetId).delete()
    ADI_media.query.filter_by(assetId=assetId).delete()
    ADI_offer.query.filter_by(assetId=assetId).delete()
    ADI_metadata.query.filter_by(assetId=assetId).delete()
    ADI_EST_Show.query.filter_by(assetId=assetId).delete()
    EST_PO.query.filter_by(assetId=assetId).delete()
    db.session.commit()

def delete_asset_standard(assetId):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function to delete the Standard Assets
    :access: public.
    :param assetId: This is the Standard Asset ID
    :return: commit delete transaction
    """
    ADI_main.query.filter_by(assetId=assetId).delete()
    ADI_media.query.filter_by(assetId=assetId).delete()
    ADI_offer.query.filter_by(assetId=assetId).delete()
    ADI_metadata.query.filter_by(assetId=assetId).delete()
    ADI_EST_Show.query.filter_by(assetId=assetId).delete()
    EST_PO.query.filter_by(assetId=assetId).delete()
    db.session.commit()


def delete_asset_est_episode(assetId):
    """
    :author: Krishnendu Banerjee.
    :date: 29/11/2019.
    :description: Function to delete the EST Episodes
    :access: public.
    :param assetId: This is the asset ID for the EST Episode
    :return: commit delete transaction
    """
    ADI_main.query.filter_by(assetId=assetId).delete()
    ADI_media.query.filter_by(assetId=assetId).delete()
    ADI_offer.query.filter_by(assetId=assetId).delete()
    ADI_metadata.query.filter_by(assetId=assetId).delete()
    ADI_EST_Show.query.filter_by(assetId=assetId).delete()
    db.session.commit()


