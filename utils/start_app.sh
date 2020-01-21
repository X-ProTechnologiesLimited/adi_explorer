#!/usr/bin/env bash
filestamp=`date +%H%M%S`
filename=adi_app.log
get_project_dir() { # Gets the root directory of the repository
    cd "${BASH_SOURCE[0]%*/*}/.." && pwd
}
if [[ $CONTAINERISED != "true" ]] ; then
    PROJECT_DIR=$(get_project_dir)
    FLASK_HOST_NAME='localhost'
    cp $PROJECT_DIR/utils/config.properties $PROJECT_DIR/lib/movie_config.py
else
    PROJECT_DIR="/app"
    FLASK_HOST_NAME='host.docker.internal'
    cp $PROJECT_DIR/utils/docker_config.properties $PROJECT_DIR/lib/movie_config.py
fi

mkdir -p $PROJECT_DIR/logs
mkdir -p $PROJECT_DIR/supp_files
mkdir -p $PROJECT_DIR/dpl_files
mkdir -p $PROJECT_DIR/created_package


echo "Starting the ADI Manager App..."
echo "Starting the ADI Manager App..." >> $PROJECT_DIR/logs/$filename
echo
source $PROJECT_DIR/utils/app_run.config && export $(cut -d= -f1 $PROJECT_DIR/utils/app_run.config)
if [ "$DATABASE_NEW" = 1 ]
then
    source $PROJECT_DIR/utils/app_run.config && export $(cut -d= -f1 $PROJECT_DIR/utils/app_run.config)
    rm -rf $PROJECT_DIR/lib/db.sqlite
    python $PROJECT_DIR/initialise_db.py
    echo "Created new database for application..."
    echo "Created new database for application..." >> $PROJECT_DIR/logs/$filename
    python -m flask run --host=0.0.0.0 >> $PROJECT_DIR/logs/$filename 2>&1 &
     
elif [ "$DATABASE_NEW" = 0 ]
then
    source $PROJECT_DIR/utils/app_run.config && export $(cut -d= -f1 $PROJECT_DIR/utils/app_run.config)
    echo "Using the existing database..."
    echo "Using the existing database..." >> $PROJECT_DIR/logs/$filename
    python -m flask run --host=0.0.0.0>> $PROJECT_DIR/logs/$filename 2>&1 &

else
    echo "Error: No Database Creation option specified.."
    exit
fi

echo "Wating for the application to initialise...."
sleep 10
echo "Application Started Successfully"
echo "Container for ADI Manager Started successfully. ADI Manager API is ready to serve http requests now...."
echo "To Shutdown Container, press Ctrl+C AND run /utils/shutdown.sh (For Standalone and Detached Containers)"
trap printout SIGINT
    printout() {
       echo ""
       echo "Shutting Down Container..User Interrupted Container"
       sleep 5
       exit
    }
    while true ; do continue ; done
# For Development and Debug Purposes, to keep the container running, uncomment the following line
#tail -200f $PROJECT_DIR/logs/$filename
