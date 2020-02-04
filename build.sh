#!/bin/bash
mkdir -p logs
. utils/app_run.config && export $(cut -d= -f1 utils/app_run.config)
#Building the Image

docker build -f Dockerfile --tag=adi_app .
docker run --rm -it --name adi_explorer --name adi_explorer -d -p $FLASK_RUN_PORT:$FLASK_RUN_PORT -it adi_app /bin/bash
echo "Now loading default image data..."
sleep 5
if [ "$DATABASE_NEW" = 1 ]
then
  echo "Loading Default Media Data..."
  curl "http://localhost:$FLASK_RUN_PORT/load_defaults"
  sleep 5
  echo "Default Media data loaded successfully.."
else
  echo "Existing Database Loaded Successfully..."
fi
# Deleting any untagged image loaded.
docker image rm `docker images | grep 'none' | awk -F ' ' '{print $3}'`
