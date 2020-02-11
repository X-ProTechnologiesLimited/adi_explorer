# models.py
from . import db

class ADI_main(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    assetId = db.Column(db.String(100), unique=True)
    original_timestamp = db.Column(db.String(100))
    adi_type = db.Column(db.String(100))
    provider_version = db.Column(db.String(100))
    provider_id = db.Column(db.String(100))
    multiformat_id = db.Column(db.String(100))

class ADI_metadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    assetId = db.Column(db.String(100), unique=True)
    title = db.Column(db.String(200))
    par_rating = db.Column(db.String(10))
    btc_rating = db.Column(db.String(10))
    audio_type = db.Column(db.String(100))
    frame_rate = db.Column(db.String(100))
    subtitle_flag = db.Column(db.String(10))
    video_type = db.Column(db.String(10))
    synopsis = db.Column(db.String(500))
    genre = db.Column(db.String(10))
    production_year = db.Column(db.String(10))
    duration = db.Column(db.String(10))
    svod_episode_name = db.Column(db.String(100))
    svod_season_number = db.Column(db.String(10))
    svod_episode_number = db.Column(db.String(10))
    svod_total_episodes = db.Column(db.String(10))
    total_asset_parts = db.Column(db.String(10))
    dpl_template = db.Column(db.String(100))
    title_filter = db.Column(db.String(10))

class ADI_offer(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    assetId = db.Column(db.String(100))
    licenseEndTime = db.Column(db.String(100))
    offer_type = db.Column(db.String(100))
    offerStartTime = db.Column(db.String(100))
    offerEndTime = db.Column(db.String(100))
    epgTime = db.Column(db.String(100))
    service_key = db.Column(db.String(10))
    est_offerId = db.Column(db.String(100))
    est_order_type = db.Column(db.String(100))


class EST_PO(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    assetId = db.Column(db.String(100))
    poption_Id = db.Column(db.String(100), unique=True)
    poption_media_type = db.Column(db.String(10))
    poption_media_filter = db.Column(db.String(10))
    uk_std_price = db.Column(db.String(10))
    uk_vip_price = db.Column(db.String(10))
    il_std_price = db.Column(db.String(10))
    il_vip_price = db.Column(db.String(10))


class ADI_media(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    assetId = db.Column(db.String(100), unique=True)
    video_path = db.Column(db.String(500))
    image_path = db.Column(db.String(500))
    movie_url = db.Column(db.String(500))
    movie_checksum = db.Column(db.String(100))
    trailer_url = db.Column(db.String(500))
    trailer_checksum = db.Column(db.String(100))
    image_url_1 = db.Column(db.String(100))
    image_checksum_1 = db.Column(db.String(100))
    image_url_2 = db.Column(db.String(100))
    image_checksum_2 = db.Column(db.String(100))
    image_url_3 = db.Column(db.String(100))
    image_checksum_3 = db.Column(db.String(100))
    image_url_4 = db.Column(db.String(100))
    image_checksum_4 = db.Column(db.String(100))
    image_url_5 = db.Column(db.String(100))
    image_checksum_5 = db.Column(db.String(100))
    image_url_6 = db.Column(db.String(100))
    image_checksum_6 = db.Column(db.String(100))

class ADI_EST_Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    assetId = db.Column(db.String(100), unique=True)
    title = db.Column(db.String(200))
    no_of_seasons = db.Column(db.String(10))
    no_of_episodes = db.Column(db.String(10))
    season_number = db.Column(db.String(10))
    episode_number = db.Column(db.String(10))
    parent_group_id = db.Column(db.String(100))
    show_type = db.Column(db.String(10))

class ADI_INGEST_HISTORY(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    assetId = db.Column(db.String(100))
    provider_version = db.Column(db.String(10))
    environment = db.Column(db.String(10))
    conversationId = db.Column(db.String(100))

class MEDIA_LIBRARY(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    filename = db.Column(db.String(100), unique=True)
    checksum = db.Column(db.String(100))
    image_group = db.Column(db.String(100))

class MEDIA_DEFAULT(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # primary keys are required by SQLAlchemy
    default_video_path = db.Column(db.String(500))
    default_image_path = db.Column(db.String(500))
    hdr_movie_file = db.Column(db.String(500))
    sdr_movie_file = db.Column(db.String(500))
    hd_movie_file = db.Column(db.String(500))
    est_movie_file = db.Column(db.String(500))
    title_movie_file = db.Column(db.String(500))
    dpl_movie_file = db.Column(db.String(500))
    trailer_file = db.Column(db.String(500))
    standard_image_file_prefix = db.Column(db.String(100))
    dpl_image_file_prefix = db.Column(db.String(100))


