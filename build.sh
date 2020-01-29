#!/bin/bash
mkdir -p logs
. utils/app_run.config && export $(cut -d= -f1 utils/app_run.config)
#Building the Image

docker build -f Dockerfile --tag=adi_app .
docker run --rm -it --name adi_explorer --name adi_explorer -d -p $FLASK_RUN_PORT:$FLASK_RUN_PORT -it adi_app /bin/bash
echo "Now loading default image data..."
sleep 5
curl 'http://localhost:5000/load_defaults'
