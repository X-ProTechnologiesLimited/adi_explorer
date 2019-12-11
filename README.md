# ADI EXPLORER
A Project to Create and Manage ADI Packages for assets. This will allow you to create, update and download ADI files for
different type of assets

## Running Locally
1. Download and Install Python 3+ from `https://www.python.org/downloads/`
2. Install git bash from `https://gitforwindows.org/`
3. Clone the ADI Explorer git repo by opening the git bash as administrator
`git clone https://github.com/X-ProTechnologiesLimited/adi_explorer.git`
4. Go to the folder adi_explorer. `cd adi_explorer` from git bash command line
5. Go to the utils directory. `cd utils`
6. Run the script `./start_app.sh`

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
1. Edit the `<adi_explorer_project_root>/lib/movie_config.py` file to refer the correct files, checksum and location
of the Media files (video files)

## Sqlite database browsing
Download the optional Sqlite DB Browser `https://sqlitebrowser.org/dl/` to browse the database file for the tool:
`<adi_explorer_project_root>/lib/db.sqlite`

## Current Scope for the tool
1. Create Single Title ADIs
2. Update Metadata for Single Title ADIs
3. Update Video for Single Title ADIs
4. View and Filter list of created ADIs
5. Download created ADI

## Enhancements Planned
1. Creating Show, Seasons and Episodes for Box Sets
2. DPL
3. Catchup
4. Update additional metadata





