from .db_create_asset import add_purchase_option
from . import db, movie_config
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




