# Filename copy_to_tank.py
# This function allows to copy Files from Local Tool Library to the Tank Location

import paramiko
from paramiko import SSHClient
from scp import SCPClient
from . import movie_config, response, errorchecker, main
from .metadata_params import metadata_default_params
from flask import request
UPLOAD_DIRECTORY = movie_config.premium_upload_dir
VRP_DIRECTORY = movie_config.premium_vrp_dir
tank_params = metadata_default_params()
tank_hostname = movie_config.tank_host


def scp_to_tank():
    filename = request.form.get('filename')
    file_type = request.form.get('file_type')
    environment = request.form.get('tank_env')
    username = request.form.get('username')
    password = request.form.get('password')
    path = request.form.get('path')
    if environment == "" and path == "":
        return errorchecker.input_missing('Tank Path or Environment')

    tank_params.tank_entry(environment, file_type, path)
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(tank_hostname, username=username, password=password, look_for_keys=False)
    except:
        return errorchecker.upload_authentication_error()

    try:
        with SCPClient(ssh.get_transport()) as scp:
            if file_type == 'VRP TAR':
                try:
                    scp.put(VRP_DIRECTORY + '/' + filename, recursive=True, remote_path=tank_params.tank_path)
                    return response.file_upload_successful(filename, environment)
                except FileNotFoundError:
                    return errorchecker.upload_filenotfound_error(filename)
            else:
                try:
                    scp.put(UPLOAD_DIRECTORY + '/' + filename, recursive=True, remote_path=tank_params.tank_path)
                    return response.file_upload_successful(filename,environment)
                except FileNotFoundError:
                    return errorchecker.upload_filenotfound_error(filename)
    except:
        return errorchecker.upload_authentication_error()


def scp_default_video_from_tank():
    username = request.form.get('username')
    password = request.form.get('password')
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    filelist = ['HDR_MOVIE.ts', 'HD_MOVIE.ts', '4K_SDR_MOVIE.ts', 'FinestHours_Trailer.ts', 'SD_2.5_min.ts', 'DPL_VIDEO_FILE.ts']
    try:
        ssh.connect(tank_hostname, username=username, password=password, look_for_keys=False)
    except:
        return errorchecker.upload_authentication_error()

    # with SCPClient(ssh.get_transport()) as scp:
    #     scp.get('/ifs/PDLTankTest/Providers/BSS/Content/Distribution/TestFiles/HD_MOVIE.ts', UPLOAD_DIRECTORY + '/', recursive=True )
    #     return main.list_files()

    for filename in filelist:
        try:
            with SCPClient(ssh.get_transport()) as scp:
                try:
                    scp.get('/ifs/PDLTankTest/Providers/BSS/Content/Distribution/TestFiles/' + filename,
                            UPLOAD_DIRECTORY + '/', recursive=True)
                except FileNotFoundError:
                    return errorchecker.upload_filenotfound_error(filename)

        except:
            return errorchecker.upload_authentication_error()

    return main.list_files()



