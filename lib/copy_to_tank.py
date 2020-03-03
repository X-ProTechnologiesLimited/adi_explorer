# Filename copy_to_tank.py
# This module allows the file transfer between the tool and the tank

import paramiko, os, sys
from paramiko import SSHClient
from scp import SCPClient
from . import movie_config, response, errorchecker, main
from .metadata_params import metadata_default_params
from flask import request
# Setting up the file transfer directories
UPLOAD_DIRECTORY = movie_config.premium_upload_dir
VRP_DIRECTORY = movie_config.premium_vrp_dir
tank_params = metadata_default_params()
tank_hostname = movie_config.tank_host

def progress(filename, size, sent):
    sys.stdout.write("%s\'s progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )

def progress4(filename, size, sent, peername):
    sys.stdout.write("(%s:%s) %s\'s progress: %.2f%%   \r" % (peername[0], peername[1], filename, float(sent)/float(size)*100) )


def scp_to_tank():  # This function copies files from tool library to Tank
    # Taking inputs from Form
    filename = request.form.get('filename')
    file_type = request.form.get('file_type')
    environment = request.form.get('tank_env')
    username = request.form.get('username')
    password = request.form.get('password')
    path = request.form.get('path')
    if environment == "" and path == "":  # Error handling missing parameters in form
        return errorchecker.input_missing('Tank Path or Environment')

    tank_params.tank_entry(environment, file_type, path)
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(tank_hostname, username=username, password=password, look_for_keys=False)
    except:
        return errorchecker.upload_authentication_error()
    files_to_copy = [f for f in os.listdir(UPLOAD_DIRECTORY) if f.startswith(filename[:-1])]  # Handling wildcard

    try:
        with SCPClient(ssh.get_transport()) as scp:
            if file_type == 'VRP TAR':
                try:
                    scp.put(VRP_DIRECTORY + '/' + filename, recursive=True, remote_path=tank_params.tank_path)
                    return response.file_upload_successful(filename, environment)
                except FileNotFoundError:
                    return errorchecker.upload_filenotfound_error(filename)
            elif file_type == 'Video':
                try:
                    scp.put(UPLOAD_DIRECTORY + '/' + filename, recursive=True, remote_path=tank_params.tank_path)
                    return response.file_upload_successful(filename,environment)
                except FileNotFoundError:
                    return errorchecker.upload_filenotfound_error(filename)
            else:
                for item in files_to_copy:  # Handling wildcard transfer of each matching files
                    try:
                        scp.put(UPLOAD_DIRECTORY + '/' + item, recursive=True, remote_path=tank_params.tank_path)
                    except FileNotFoundError:
                        return errorchecker.upload_filenotfound_error(item)

                return response.file_upload_successful(item, environment)
    except:
        return errorchecker.upload_authentication_error()



def scp_default_video_from_tank():  # This function copies default video files from Tank to Tool Library
    # Taking inputs from Form
    username = request.form.get('username')
    password = request.form.get('password')
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Default File Lists to be copied. Retrieving from the config.
    filelist = movie_config.default_file_list
    try:
        ssh.connect(tank_hostname, username=username, password=password, look_for_keys=False)
    except:
        return errorchecker.upload_authentication_error()

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

def scp_file_from_tank(tank_path, filename):  # This function copies local files in tool to Tank
    # Taking inputs from Form
    username = request.form.get('username')
    password = request.form.get('password')
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(tank_hostname, username=username, password=password, look_for_keys=False)
    except:
        return errorchecker.upload_authentication_error()


    try:
        with SCPClient(ssh.get_transport(), sanitize=lambda x: x) as scp:  # Handling Wildcard Transfers
            try:
                scp.get(tank_path + '/' + filename[:-1] + '*', UPLOAD_DIRECTORY + '/', recursive=True)
            except FileNotFoundError:
                return errorchecker.upload_filenotfound_error(filename)

    except:
        return errorchecker.upload_authentication_error()

    return main.list_files()