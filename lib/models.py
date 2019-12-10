# models.py
from . import db

class ADI_META(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    assetId = db.Column(db.String(100), unique=True)
    original_timestamp = db.Column(db.String(100))
    adi_type = db.Column(db.String(100))
    title = db.Column(db.String(200))
    provider_version = db.Column(db.String(100))
    provider_id = db.Column(db.String(100))
    licenseEndTime = db.Column(db.String(100))
    offer_type = db.Column(db.String(100))
    offerStartTime = db.Column(db.String(100))
    offerEndTime = db.Column(db.String(100))
    multiformat_id = db.Column(db.String(100))
    movie_url = db.Column(db.String(500))
    movie_checksum = db.Column(db.String(500))
    par_rating = db.Column(db.String(10))
    btc_rating = db.Column(db.String(10))
    audio_type = db.Column(db.String(100))
    frame_rate = db.Column(db.String(100))
    subtitle_flag = db.Column(db.String(10))
    video_type = db.Column(db.String(10))
    synopsis = db.Column(db.String(500))
    production_year = db.Column(db.String(500))

