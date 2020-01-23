from . import main
import subprocess
from flask import request
import requests
from . import movie_config
from .models import ADI_main
from . import errorchecker

UPLOAD_DIRECTORY = movie_config.premium_upload_dir
VRP_PACKAGE_DIR = movie_config.premium_vrp_dir

def make_tarfile():
    output_filename = request.form.get('filename')
    assetId = request.form.get('assetId')
    video_type = request.form.get('video_type')
    tar_filename = VRP_PACKAGE_DIR+'/'+output_filename
    if assetId != "":
        my_filename = movie_config.premium_upload_dir + '/ADI.xml'
        package = ADI_main.query.filter_by(assetId=assetId).first()
        if 'VRP' not in package.adi_type:
            return errorchecker.use_different_method(package.adi_type)

        get_adi_url = 'http://localhost:5000/get_adi/' + assetId
        response_adi = requests.get(url=get_adi_url)
        with open(my_filename, 'w') as f:
            f.write(response_adi.text)

        if (video_type == 'HD') and (('hd.' in package.provider_id) or ('_hd' in package.provider_id)):
            media_file = movie_config.hd_movie_file
        elif (video_type == 'SDR') and ('4k' in package.provider_id):
            media_file = movie_config.sdr_movie_file
        elif (video_type == 'HDR') and ('hdr' in package.provider_id):
            media_file = movie_config.hdr_movie_file
        else:
            return errorchecker.internal_server_error_show(video_type)

        subprocess.call(['tar', '-C', UPLOAD_DIRECTORY, '-cf', tar_filename, 'FinestHours_182x98.jpg',
                             'FinestHours_182x243.jpg', 'FinestHours_262x349.jpg', 'FinestHours_456x257.jpg',
                             'FinestHours_Trailer.ts', media_file, 'ADI.xml'])
        return main.send_tar_file(output_filename)

    else:
        if video_type == 'HD':
            media_file = movie_config.hd_movie_file
        elif video_type == 'SDR':
            media_file = movie_config.sdr_movie_file
        elif video_type == 'HDR':
            media_file = movie_config.hdr_movie_file
        else:
            return errorchecker.internal_server_error_show(video_type)

        subprocess.call(['tar', '-C', UPLOAD_DIRECTORY, '-cf', tar_filename, 'FinestHours_182x98.jpg',
                             'FinestHours_182x243.jpg', 'FinestHours_262x349.jpg', 'FinestHours_456x257.jpg',
                             'FinestHours_Trailer.ts', media_file, 'ADI.xml'])
        return main.send_tar_file(output_filename)