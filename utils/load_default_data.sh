#!/bin/bash
get_project_dir() { # Gets the root directory of the repository
    cd "${BASH_SOURCE[0]%*/*}/.." && pwd
}
if [[ $(docker ps | grep adi_explorer | awk -F ' ' '{print $1}') ]]; then
    PROJECT_DIR="/app"
    echo "Loading Default Data file"
    sleep 5
    docker cp config.properties `docker ps | grep adi_explorer | awk -F ' ' '{print $1}'`:/app/lib/movie_config.py
else
    PROJECT_DIR=$(get_project_dir)
    echo "Loading Default Data file"
    sleep 5
    cp config.properties $PROJECT_DIR/lib/movie_config.py
fi