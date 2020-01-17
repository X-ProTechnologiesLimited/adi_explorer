from . import main
from . import errorchecker
import subprocess
from flask import request
from . import movie_config

UPLOAD_DIRECTORY = movie_config.premium_upload_dir
VRP_PACKAGE_DIR = movie_config.premium_vrp_dir

def make_tarfile_premium():
    output_filename = request.form.get('filename')
    video_type = request.form.get('video_type')
    tar_filename = VRP_PACKAGE_DIR+'/'+output_filename
    if video_type == 'HD':
        subprocess.call(['tar', '-C', UPLOAD_DIRECTORY, '-cf', tar_filename, 'FinestHours_182x98.jpg',
                         'FinestHours_182x243.jpg', 'FinestHours_262x349.jpg', 'FinestHours_456x257.jpg',
                         'FinestHours_Trailer.ts', 'HD_MOVIE.ts', 'ADI.xml'])
        return main.send_tar_file(output_filename)
    elif video_type == 'SDR':
        subprocess.call(
            ['tar', '-C', UPLOAD_DIRECTORY, '-cf', tar_filename, 'FinestHours_182x98.jpg',
              'FinestHours_182x243.jpg', 'FinestHours_262x349.jpg', 'FinestHours_456x257.jpg',
              'FinestHours_Trailer.ts', 'CATS_EP1_UHD_3170_1mins.ts', 'ADI.xml'])
        return main.send_tar_file(output_filename)
    elif video_type == 'HDR':
        subprocess.call(
            ['tar', '-C', UPLOAD_DIRECTORY, '-cf', tar_filename, 'FinestHours_182x98.jpg',
              'FinestHours_182x243.jpg', 'FinestHours_262x349.jpg', 'FinestHours_456x257.jpg',
              'FinestHours_Trailer.ts', 'IdentExternalDDplus_MainWithExternalAtmos_IdentExternalDDplus-Ateme_out_API.ts', 'ADI.xml'])
        return main.send_tar_file(output_filename)
    else:
        return errorchecker.internal_server_error_show(video_type)
