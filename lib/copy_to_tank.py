import paramiko
from paramiko import SSHClient
from scp import SCPClient
from . import movie_config, response, errorchecker
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
    ssh.connect(tank_hostname, username=username, password=password, look_for_keys=False)

    try:
        with SCPClient(ssh.get_transport()) as scp:
            if file_type == 'VRP TAR':
                scp.put(VRP_DIRECTORY + '/' + filename, recursive=True, remote_path=tank_params.tank_path)
                return response.file_upload_successful(filename, environment)
            else:
                scp.put(UPLOAD_DIRECTORY + '/' + filename, recursive=True, remote_path=tank_params.tank_path)
                return response.file_upload_successful(filename,environment)
    except:
        return errorchecker.upload_unsuccessful()
