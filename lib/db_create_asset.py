
from .models import ADI_main, ADI_metadata, ADI_offer, ADI_media, ADI_EST_Show, MEDIA_DEFAULT, EST_PO
from . import db
from .est_show_params import est_show_default_params
from .metadata_params import metadata_default_params
from .image_params import image_default_params


# Call Parameter Functions - These are functions to load default parameter values unless supplied in request
est_params = est_show_default_params()
params = metadata_default_params()  # Checking Default Param Value if Form entry is null
image_set = image_default_params()  # Image classification function

def add_media(provider_id, asset_type, assetId):
    params.movie_details_entry(provider_id, asset_type)
    params.trailer_entry()
    image_set.image_entry(asset_type)
    path_default = MEDIA_DEFAULT.query.first()

    new_package_media = ADI_media(assetId=assetId, video_path=path_default.default_video_path,
                                  image_path=path_default.default_image_path, movie_url=params.asset_media['movie_url'],
                                  movie_checksum=params.asset_media['movie_checksum'],
                                  trailer_url=params.asset_media['trailer_file'],
                                  trailer_checksum=params.asset_media['trailer_checksum'],
                                  image_url_1=image_set.asset_image['image_1'],
                                  image_checksum_1=image_set.asset_image['image_1_checksum'],
                                  image_url_2=image_set.asset_image['image_2'],
                                  image_checksum_2=image_set.asset_image['image_2_checksum'],
                                  image_url_3=image_set.asset_image['image_3'],
                                  image_checksum_3=image_set.asset_image['image_3_checksum'],
                                  image_url_4=image_set.asset_image['image_4'],
                                  image_checksum_4=image_set.asset_image['image_4_checksum'],
                                  image_url_5=image_set.asset_image['image_5'],
                                  image_checksum_5=image_set.asset_image['image_5_checksum'],
                                  image_url_6=image_set.asset_image['image_6'],
                                  image_checksum_6=image_set.asset_image['image_6_checksum'])

    db.session.add(new_package_media)
    db.session.commit()

def add_main(assetId, asset_timestamp, adi_type, provider_version, provider_id, multiformat_id=""):
    new_asset_main = ADI_main(assetId=assetId, original_timestamp=asset_timestamp,
                              adi_type=adi_type, provider_version=provider_version,
                              provider_id=provider_id, multiformat_id=multiformat_id)

    db.session.add(new_asset_main)
    db.session.commit()

def add_meta(assetId, title, synopsis, par_rating, title_filter, subtitle_flag="", audio_type="", frame_rate="",
             btc_rating="", video_type="", production_year="", genre="", duration="", svod_episode_name="",
             svod_season_number="", svod_episode_number="", svod_total_episodes="", total_asset_parts="",
             dpl_template=""):
    new_asset_meta = ADI_metadata(assetId=assetId, title=title, synopsis=synopsis, par_rating=par_rating,
                                  title_filter=title_filter, subtitle_flag=subtitle_flag,
                                  audio_type=audio_type, frame_rate=frame_rate, btc_rating=btc_rating,
                                  video_type=video_type, production_year=production_year, genre=genre,
                                  duration=duration, svod_episode_name=svod_episode_name,
                                  svod_season_number=svod_season_number, svod_episode_number=svod_episode_number,
                                  svod_total_episodes=svod_total_episodes, total_asset_parts=total_asset_parts,
                                  dpl_template=dpl_template)

    db.session.add(new_asset_meta)
    db.session.commit()

def add_offer(assetId, offer_type, offerStartTime, offerEndTime, licenseEndTime, service_key="", epgTime="",
              est_offerId="", est_order_type=""):

    new_asset_offer = ADI_offer(assetId=assetId, offer_type=offer_type, offerStartTime=offerStartTime,
                                offerEndTime=offerEndTime, licenseEndTime=licenseEndTime, service_key=service_key,
                                epgTime=epgTime, est_offerId=est_offerId, est_order_type=est_order_type)

    db.session.add(new_asset_offer)
    db.session.commit()


def add_group(assetId, title, show_type, no_of_seasons="", no_of_episodes="", season_number="", episode_number="",
              parent_group_id=""):

    new_asset_group = ADI_EST_Show(assetId=assetId, title=title, show_type=show_type, no_of_seasons=no_of_seasons,
                                   no_of_episodes=no_of_episodes, season_number=season_number,
                                   episode_number=episode_number, parent_group_id=parent_group_id)

    db.session.add(new_asset_group)
    db.session.commit()


def add_purchase_option(assetId, poption_Id, poption_media_type, poption_media_filter, uk_std_price, uk_vip_price,
                        il_std_price, il_vip_price):

    new_asset_po = EST_PO(assetId=assetId, poption_Id=poption_Id, poption_media_type=poption_media_type,
                          poption_media_filter=poption_media_filter, uk_std_price=uk_std_price,
                          uk_vip_price=uk_vip_price, il_std_price=il_std_price, il_vip_price=il_vip_price)

    db.session.add(new_asset_po)
    db.session.commit()
