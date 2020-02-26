# Filename create_est_order_type.py
# This module is responsible for creating different order types (PreOrder/ComingSoon/Regular) for EST Assets

from .models import ADI_offer
from . import db
from .est_show_params import est_show_default_params
from .metadata_params import metadata_default_params
from flask import request
est_params = est_show_default_params()
params = metadata_default_params()

def create_est_orders(asset_timestamp, licenseEndTime, order_type, asset_type):
    est_params.est_offer_window_entry(request.form.get('po_offer_window'), request.form.get('cs_offer_window'),
                                      request.form.get('reg_offer_window'))
    est_params.est_offer_date_entry(order_type, est_params.po_offer_window, est_params.cs_offer_window,
                                    est_params.reg_offer_window)
    if asset_type == 'EST SINGLE TITLE':
        params.offer_type_entry(asset_type)
        assetId = asset_timestamp + '01'
    elif asset_type == 'est_show':
        params.offer_type_entry(asset_type)
        assetId = asset_timestamp + '00'
    else:
        return 'incorrect asset type'

    if order_type == "PO":
        new_package_offer_PO = ADI_offer(assetId=assetId, offer_type=params.offer_type,
                                         offerStartTime=est_params.po_start, offerEndTime=est_params.po_end,
                                         licenseEndTime=licenseEndTime, est_order_type='PreOrder',
                                         est_offerId=asset_timestamp + '01')

        db.session.add(new_package_offer_PO)
    elif order_type == "REG":
        new_package_offer_REG = ADI_offer(assetId=assetId, offer_type=params.offer_type,
                                         offerStartTime=est_params.reg_start, offerEndTime=est_params.reg_end,
                                         licenseEndTime=licenseEndTime, est_order_type='Regular',
                                         est_offerId=asset_timestamp + '01')

        db.session.add(new_package_offer_REG)

    elif order_type == "PO+CS":
        new_package_offer_CS = ADI_offer(assetId=assetId, offer_type=params.offer_type,
                                         offerStartTime=est_params.cs_start, offerEndTime=est_params.cs_end,
                                         licenseEndTime=licenseEndTime, est_order_type='ComingSoon',
                                         est_offerId=asset_timestamp + '01')

        new_package_offer_PO = ADI_offer(assetId=assetId, offer_type=params.offer_type,
                                         offerStartTime=est_params.po_start, offerEndTime=est_params.po_end,
                                         licenseEndTime=licenseEndTime, est_order_type='PreOrder',
                                         est_offerId=asset_timestamp + '02')

        db.session.add_all([new_package_offer_CS, new_package_offer_PO])

    elif order_type == 'PO+CS+REG':
        new_package_offer_REG = ADI_offer(assetId=assetId, offer_type=params.offer_type,
                                          offerStartTime=est_params.reg_start, offerEndTime=est_params.reg_end,
                                          licenseEndTime=licenseEndTime, est_order_type='Regular',
                                          est_offerId=asset_timestamp + '01')
        db.session.add(new_package_offer_REG)

        new_package_offer_CS = ADI_offer(assetId=assetId, offer_type=params.offer_type,
                                         offerStartTime=est_params.cs_start, offerEndTime=est_params.cs_end,
                                         licenseEndTime=licenseEndTime, est_order_type='ComingSoon',
                                         est_offerId=asset_timestamp + '02')
        db.session.add(new_package_offer_CS)

        new_package_offer_PO = ADI_offer(assetId=assetId, offer_type=params.offer_type,
                                         offerStartTime=est_params.po_start, offerEndTime=est_params.po_end,
                                         licenseEndTime=licenseEndTime, est_order_type='PreOrder',
                                         est_offerId=asset_timestamp + '03')
        db.session.add_all([new_package_offer_REG, new_package_offer_CS, new_package_offer_PO])

    else:
        return 'incorrect order type'

    db.session.commit()




