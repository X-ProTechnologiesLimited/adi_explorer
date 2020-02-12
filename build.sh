#!/bin/bash
mkdir -p logs
. utils/app_run.config && export $(cut -d= -f1 utils/app_run.config)
cp utils/Dockerfile.local Dockerfile


if [[ $1 == "--new-db" ]];then
  echo -e '\nENTRYPOINT ["utils/start_app_docker.sh", "--new-db"]' >> Dockerfile
elif [[ "$1" == '' ]];then
  echo -e '\nENTRYPOINT ["utils/start_app_docker.sh", "--old-db"]' >> Dockerfile
else
  echo "Error: Incorrect Database Creation option specified.."
  printf "Please use correct flags for database creation...\n"
  printf "build.sh --new-db : [This will create a new database before starting the app]\n"
  printf "build.sh <no input> : [This will use existing/old database before starting the app]\n"
  exit
fi


#Building the Image
docker build -f Dockerfile --tag=adi_app .

# Running the Container
docker run --rm -it --name adi_explorer --name adi_explorer -d -p $FLASK_RUN_PORT:$FLASK_RUN_PORT -it adi_app /bin/bash


## Deleting any untagged loaded image to keep Docker clean
docker image rm -f `docker images | grep 'none' | awk -F ' ' '{print $3}'`
printf "Removed unnecessary images\n"

# Remove Dockerfile
rm -rf Dockerfile
