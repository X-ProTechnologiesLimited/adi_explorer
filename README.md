# ADI EXPLORER
A Project to Create and Manage ADI Packages for assets. This will allow you to create, update and download ADI files for
different type of assets

## Running Locally
1. Download and Install Python 3+ from `https://www.python.org/downloads/`
2. Install git bash from `https://gitforwindows.org/`
3. Clone the ADI Explorer git repo by opening the git bash as administrator
`git clone https://github.com/X-ProTechnologiesLimited/adi_explorer.git`
4. Go to the folder adi_explorer. `cd adi_explorer` from git bash command line
5. Run the command `pip3 install -r requirements.txt`
6. Go to the utils directory. `cd utils`
7. Run the script `./start_app.sh --new-db` to create a new database instance OR `./start_app.sh --old-db`
to use an existing database from pre-run.

## Running in Container
The project is also enabled to run in Docker Container. It contains the Dockerfile

### MAC / Unix
1. Install Docker for MAC / Unix
2. Clone the repo `git clone https://github.com/X-ProTechnologiesLimited/adi_explorer.git` from terminal
3. Run the `./build.sh` script in the project root (adi_explorer)

### Windows: Install Docker for Windows (Windows 10 onwards)
1. Install Docker Desktop for windows `https://hub.docker.com/editions/community/docker-ce-desktop-windows`
2. Install the Windows Ubuntu App from Windows App Store. Follow instructions from
 `https://docs.microsoft.com/en-us/windows/wsl/install-win10`
3. Install Docker Engine on Ubuntu App and configure with Windows Docker Desktop. Follow instructions from
`https://medium.com/@sebagomez/installing-the-docker-client-on-ubuntus-windows-subsystem-for-linux-612b392a44c4`
4. Clone the repo `git clone https://github.com/X-ProTechnologiesLimited/adi_explorer.git` from terminal
5. Run the `./build.sh` script in the project root (adi_explorer)

## Configuring the Media Paths for Test Environments
1. Edit the `<adi_explorer_project_root>/utils/config.properties` file to refer the correct files, checksum and location
of the Media files (video files) based on Test Environment Tank file locations
2. Edit the same file for default metadata

## Sqlite database browsing
Download the optional Sqlite DB Browser `https://sqlitebrowser.org/dl/` to browse the database file for the tool:
`<adi_explorer_project_root>/lib/db.sqlite`

## Current Scope for the tool
1. Create Single Title ADIs and VRP Packages
2. Create EST Episodes, Shows and Seasons
3. Update Metadata for Single Title ADIs and EST Assets
4. Update Video for Single Title ADIs and Episodes
5. View and Filter list of created ADIs and EST Shows
6. Download created ADIs for Title, Episode and Shows
7. Ingest ADI into test environments directly from tool
8. Upload new media files and calculate checksum
9. Upload Media and Tar files into Tank

## Enhancements Planned
1. Update additional metadata
2. Update Images
3. Cloning Assets

## Tunnelling for the tool for Ingest Purpose
Since the VAM is not reachable from Local WorkStations, we need to open a socks tunnel to VAM nodes
1. Login to any unix jump boxes and `ssh -v -N -L <vam_port>:<vam_host>:<vam_port> username@jump_host`
2. Open putty.exe and open session to same Jump box with a tunnel with source port 14231