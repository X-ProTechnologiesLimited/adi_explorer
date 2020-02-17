from .models import EST_PO
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
        new_purchase_option_dig = EST_PO(assetId=assetId, poption_Id=asset_timestamp + '01', poption_media_type='1',
                                         poption_media_filter='4', uk_std_price=movie_config.uk_std_price,
                                         uk_vip_price=movie_config.uk_vip_price, il_std_price=movie_config.il_std_price,
                                         il_vip_price=movie_config.il_vip_price)
        db.session.add(new_purchase_option_dig)

    elif order_type == 'Digital+DVD':
        new_purchase_option_dig = EST_PO(assetId=assetId, poption_Id=asset_timestamp + '01', poption_media_type='1',
                                         poption_media_filter='4', uk_std_price=movie_config.uk_std_price,
                                         uk_vip_price=movie_config.uk_vip_price, il_std_price=movie_config.il_std_price,
                                         il_vip_price=movie_config.il_vip_price)

        new_purchase_option_dvd = EST_PO(assetId=assetId, poption_Id=asset_timestamp + '02', poption_media_type='2',
                                         poption_media_filter='1', uk_std_price=uk_std_price_dvd,
                                         uk_vip_price=uk_vip_price_dvd, il_std_price=il_std_price_dvd,
                                         il_vip_price=il_std_price_dvd)

        db.session.add_all([new_purchase_option_dig, new_purchase_option_dvd])

    elif order_type == 'Digital+DVD+BluR':
        new_purchase_option_dig = EST_PO(assetId=assetId, poption_Id=asset_timestamp + '01', poption_media_type='1',
                                         poption_media_filter='4', uk_std_price=movie_config.uk_std_price,
                                         uk_vip_price=movie_config.uk_vip_price, il_std_price=movie_config.il_std_price,
                                         il_vip_price=movie_config.il_vip_price)

        new_purchase_option_dvd = EST_PO(assetId=assetId, poption_Id=asset_timestamp + '02', poption_media_type='2',
                                         poption_media_filter='1', uk_std_price=uk_std_price_dvd,
                                         uk_vip_price=uk_vip_price_dvd, il_std_price=il_std_price_dvd,
                                         il_vip_price=il_std_price_dvd)

        new_purchase_option_blu = EST_PO(assetId=assetId, poption_Id=asset_timestamp + '03', poption_media_type='3',
                                         poption_media_filter='2', uk_std_price=uk_std_price_blu,
                                         uk_vip_price=uk_vip_price_blu, il_std_price=il_std_price_blu,
                                         il_vip_price=il_std_price_blu)

        db.session.add_all([new_purchase_option_dig, new_purchase_option_dvd, new_purchase_option_blu])
        db.session.commit()

    else:
        return 'incorrect order type'




