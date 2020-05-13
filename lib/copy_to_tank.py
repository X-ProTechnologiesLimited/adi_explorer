# Filename: lib/copy_to_tank.py
"""
Created on Nov 29, 2019

@author: Krishnendu Banerjee
@summary: This file holds the functions to transfer files from local to tank and vice versa:

"""

import paramiko, os
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

def scp_to_jump():
    """
        :author: Krishnendu Banerjee.
        :date: 06/03/2019.
        :description: Function that copies the files from local tool to the Secured Jump Box
        :access: public.
        :form_input: templates/upload_to_jump.html
        """
    # Taking the host/file/user credentials input from the user input form
    filename = request.form.get('filename')
    jump_host = request.form.get('hostname')
    username = request.form.get('username')
    password = request.form.get('password')
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(jump_host, username=username, password=password, look_for_keys=False)
    except:
        return errorchecker.upload_authentication_error()

    try:
        with SCPClient(ssh.get_transport()) as scp:
            try:
                scp.put(VRP_DIRECTORY + '/' + filename, recursive=True, remote_path='/tmp')
                return response.file_upload_successful(filename)
            except FileNotFoundError:
                return errorchecker.upload_filenotfound_error(filename)

    except:
        return errorchecker.upload_authentication_error()


def scp_to_tank():
    """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function that copies the files from local tool to the Tank
        :access: public.
        :form_input: templates/upload_to_tank.html
    """
    # Taking the host/file/user credentials input from the user input form
    filename = request.form.get('filename')
    file_type = request.form.get('file_type')
    environment = request.form.get('tank_env') # Depends on which environment is chosen by user
    username = request.form.get('username')
    password = request.form.get('password')
    path = request.form.get('path') # Another option is to specify the path directly
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
                    return response.file_upload_successful(filename)
                except FileNotFoundError:
                    return errorchecker.upload_filenotfound_error(filename)
            elif file_type == 'Video':
                try:
                    scp.put(UPLOAD_DIRECTORY + '/' + filename, recursive=True, remote_path=tank_params.tank_path)
                    return response.file_upload_successful(filename)
                except FileNotFoundError:
                    return errorchecker.upload_filenotfound_error(filename)
            else:
                for item in files_to_copy:  # Handling wildcard transfer of each matching files
                    try:
                        scp.put(UPLOAD_DIRECTORY + '/' + item, recursive=True, remote_path=tank_params.tank_path)
                    except FileNotFoundError:
                        return errorchecker.upload_filenotfound_error(item)

                return response.file_upload_successful(item)
    except:
        return errorchecker.upload_authentication_error()



def scp_default_video_from_tank():
    """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function that copies the default video files from the Tank to the local tool
        :access: public.
        :form_input: templates/load_default_library.html
        """
    # Taking the host/file/user credentials input from the user input form
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

def scp_file_from_tank(tank_path, filename):
    """
        :author: Krishnendu Banerjee.
        :date: 29/11/2019.
        :description: Function that copies specific files from the Tank to the local tool
        :access: public.
        :form_input: templates/upload_files.html
        """
    # Taking the host/file/user credentials input from the user input form
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