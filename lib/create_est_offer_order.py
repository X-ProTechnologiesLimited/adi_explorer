# Filename: lib/create_est_offer_order.py
"""
Created on June 01, 2020

@author: Krishnendu Banerjee
@summary: This file holds the function to create the different Order Types and Purchase Options for EST Assets

"""

from .db_create_asset import add_offer, add_purchase_option
from . import movie_config
from .params_default import metadata_default_params, est_show_default_params
from flask import request
est_params = est_show_default_params() # Function to Load the Default EST parameters
params = metadata_default_params() # Function to load default Param Value if Form entry is null

# Load Default Pricing of the different purchase options
uk_std_price_dig = float(movie_config.uk_std_price)
uk_vip_price_dig = float(movie_config.uk_vip_price)
il_std_price_dig = float(movie_config.il_std_price)
il_vip_price_dig = float(movie_config.il_vip_price)
uk_std_price_dvd = str(float(movie_config.uk_std_price) + 10)
uk_vip_price_dvd = str(float(movie_config.uk_vip_price) + 10)
il_std_price_dvd = str(float(movie_config.il_std_price) + 10)
il_vip_price_dvd = str(float(movie_config.il_vip_price) + 10)
uk_std_price_blu = str(float(movie_config.uk_std_price) + 15)
uk_vip_price_blu = str(float(movie_config.uk_vip_price) + 15)
il_std_price_blu = str(float(movie_config.il_std_price) + 15)
il_vip_price_blu = str(float(movie_config.il_vip_price) + 15)


def create_po(order_type, asset_timestamp, asset_type):
    """
    :author: Krishnendu Banerjee.
    :date: 29/03/2020.
    :description: Creates the Purchase Options for EST Assets.
    :access: public
    :param order_type: Mandatory: Digital Only, Digital+DVD, Digital+DVD+BluR
    :param asset_timestamp: Mandatory
    :param asset_type: Mandatory: EST SINGLE TITLE, est_show
    :return: Add DB entry for EST Purchase Options successfully
    """
    if asset_type == 'EST SINGLE TITLE':
        assetId = asset_timestamp + '01'
    elif asset_type == 'est_show':
        assetId = asset_timestamp + '00'
    else:
        return 'incorrect asset type'

    if order_type == 'Digital Only':
        add_purchase_option(assetId, asset_timestamp + '01', '1', '4', movie_config.uk_std_price,
                            movie_config.uk_vip_price, movie_config.il_std_price, movie_config.il_vip_price)

    elif order_type == 'Digital+DVD':
        add_purchase_option(assetId, asset_timestamp + '01', '1', '4', movie_config.uk_std_price,
                            movie_config.uk_vip_price, movie_config.il_std_price, movie_config.il_vip_price)

        add_purchase_option(assetId, asset_timestamp + '02', '2', '1', uk_std_price_dvd,
                            uk_vip_price_dvd, il_std_price_dvd, il_vip_price_dvd)

    elif order_type == 'Digital+DVD+BluR':
        add_purchase_option(assetId, asset_timestamp + '01', '1', '4', movie_config.uk_std_price,
                            movie_config.uk_vip_price, movie_config.il_std_price, movie_config.il_vip_price)

        add_purchase_option(assetId, asset_timestamp + '02', '2', '1', uk_std_price_dvd,
                            uk_vip_price_dvd, il_std_price_dvd, il_vip_price_dvd)

        add_purchase_option(assetId, asset_timestamp + '03', '3', '2', uk_std_price_blu,
                            uk_vip_price_blu, il_std_price_blu, il_vip_price_blu)

    else:
        return 'incorrect order type'



def create_est_orders(asset_timestamp, licenseEndTime, order_type, asset_type):
    """
    :author: Krishnendu Banerjee.
    :date: 29/03/2020.
    :description: Creates the EST Offers for the EST Assets.
    :access: public
    :param asset_timestamp:
    :param licenseEndTime:
    :param order_type: PO - PreOrder, REG - Regular, PO+CS - PreOrder and ComingSoon, PO+CS+REG - PreOrder and
        ComingSoon and Regular
    :param asset_type: EST SINGLE TITLE, est_show
    :return: Add DB entry for EST Order Types successfully
    """
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

    if order_type == "PO":  # Only create one offer of Type PreOrder for the EST Asset
        add_offer(assetId, params.asset_meta['offer_type'], est_params.purchase_option_params['po_start'],
                  est_params.purchase_option_params['po_end'], licenseEndTime=licenseEndTime,
                  est_offerId=asset_timestamp + '01', est_order_type='PreOrder')
    elif order_type == "REG": # Only create one offer of Type Regular for the EST Asset
        add_offer(assetId, params.asset_meta['offer_type'], est_params.purchase_option_params['reg_start'],
                 est_params.purchase_option_params['reg_end'], licenseEndTime=licenseEndTime,
                 est_offerId=asset_timestamp + '01', est_order_type='Regular')
    elif order_type == "PO+CS": # Create 2 offers of Type PreOrder and ComingSoon for the EST Asset
        add_offer(assetId, params.asset_meta['offer_type'], est_params.purchase_option_params['cs_start'],
                  est_params.purchase_option_params['cs_end'], licenseEndTime=licenseEndTime,
                  est_offerId=asset_timestamp + '01', est_order_type='ComingSoon')
        add_offer(assetId, params.asset_meta['offer_type'], est_params.purchase_option_params['po_start'],
                  est_params.purchase_option_params['po_end'], licenseEndTime=licenseEndTime,
                  est_offerId=asset_timestamp + '02', est_order_type='PreOrder')
    elif order_type == 'PO+CS+REG': # Create 3 offers of Type PreOrder, ComingSoon and Regular for the EST Asset
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




