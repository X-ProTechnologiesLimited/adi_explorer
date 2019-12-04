#!/bin/bash
#Zip the existing logs in logs folder before copying from container
log_timestamp=`date '+%Y%m%d%H%M%S'`
gzip -S "_$log_timestamp.gz" ../logs/*.log
#Copy the database and logs from container before shutdown
if [[ $(docker ps | grep adi_explorer | awk -F ' ' '{print $1}') ]]; then
	        docker cp `docker ps | grep adi_explorer | awk -F ' ' '{print $1}'`:/app/lib/db.sqlite ../lib/
	        docker cp `docker ps | grep adi_explorer | awk -F ' ' '{print $1}'`:/app/logs/ ../
		        printf "\nData file and Logs from container copied successfully\n"
		else
			        printf "\nApplication is not running in Container, so nothing to copy\n"
			fi
echo "Calling Shutdown..."
sleep 1
. app_run.config && export $(cut -d= -f1 app_run.config)
response=$(curl --silent "http://localhost:$FLASK_RUN_PORT/quit")
if [ "$response" == "Appliation shutting down..." ];
then
  printf "\nApplication shutdown successful\n"
else
 printf "\nShutdown Error: No Flask Application Running\n"
fi

printf "\nChecking Container.....\n"

if [[ $(docker ps | grep adi_explorer | awk -F ' ' '{print $1}') ]]; then
        docker kill `docker ps | grep adi_explorer | awk -F ' ' '{print $1}'`
        printf "\nContainer Stopped Successfully\n"
else
        printf "\nNo Container is there for ADI Manager\n"
fi
