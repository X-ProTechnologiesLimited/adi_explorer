# Filename create_est_order_type.py
# This module is responsible for creating different order types (PreOrder/ComingSoon/Regular) for EST Assets

from .db_create_asset import add_offer
from .est_show_params import est_show_default_params
from .metadata_params import metadata_default_params
from flask import request
est_params = est_show_default_params()
params = metadata_default_params()

def create_est_orders(asset_timestamp, licenseEndTime, order_type, asset_type):
    est_params.est_offer_window_entry(request.form.get('po_offer_window'), request.form.get('cs_offer_window'),
                                      request.form.get('reg_offer_window'))
    est_params.est_offer_date_entry(order_type, est_params.purchase_option_params['po_offer_window'],
                                    est_params.purchase_option_params['cs_offer_window'],
                                    est_params.purchase_option_params['reg_offer_window'])

    if asset_type == 'EST SINGLE TITLE':
        params.offer_type_entry(asset_type)
        assetId = asset_timestamp + '01'
    elif asset_type == 'est_show':
        params.offer_type_entry(asset_type)
        assetId = asset_timestamp + '00'
    else:
        return 'incorrect asset type'

    if order_type == "PO":
        add_offer(assetId, params.asset_meta['offer_type'], est_params.purchase_option_params['po_start'],
                  est_params.purchase_option_params['po_end'], licenseEndTime=licenseEndTime,
                  est_offerId=asset_timestamp + '01', est_order_type='PreOrder')
    elif order_type == "REG":
        add_offer(assetId, params.asset_meta['offer_type'], est_params.purchase_option_params['reg_start'],
                 est_params.purchase_option_params['reg_end'], licenseEndTime=licenseEndTime,
                 est_offerId=asset_timestamp + '01', est_order_type='Regular')
    elif order_type == "PO+CS":
        add_offer(assetId, params.asset_meta['offer_type'], est_params.purchase_option_params['cs_start'],
                  est_params.purchase_option_params['cs_end'], licenseEndTime=licenseEndTime,
                  est_offerId=asset_timestamp + '01', est_order_type='ComingSoon')
        add_offer(assetId, params.asset_meta['offer_type'], est_params.purchase_option_params['po_start'],
                  est_params.purchase_option_params['po_end'], licenseEndTime=licenseEndTime,
                  est_offerId=asset_timestamp + '02', est_order_type='PreOrder')
    elif order_type == 'PO+CS+REG':
        add_offer(assetId, params.asset_meta['offer_type'], est_params.purchase_option_params['reg_start'],
                  est_params.purchase_option_params['reg_end'], licenseEndTime=licenseEndTime,
                  est_offerId=asset_timestamp + '01', est_order_type='Regular')
        add_offer(assetId, params.asset_meta['offer_type'], est_params.purchase_option_params['cs_start'],
                  est_params.purchase_option_params['cs_end'], licenseEndTime=licenseEndTime,
                  est_offerId=asset_timestamp + '02', est_order_type='ComingSoon')
        add_offer(assetId, params.asset_meta['offer_type'], est_params.purchase_option_params['po_start'],
                  est_params.purchase_option_params['po_end'], licenseEndTime=licenseEndTime,
                  est_offerId=asset_timestamp + '03', est_order_type='PreOrder')
    else:
        return 'incorrect order type'




