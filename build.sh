#!/bin/bash
. utils/app_run.config && export $(cut -d= -f1 utils/app_run.config)
#Building the Image
docker build -f Dockerfile --tag=adi_app .
docker run --rm -it --name adi_explorer -v $PWD/logs:/app/logs -v $PWD/lib:/app/lib/ --name adi_explorer -d -p $FLASK_RUN_PORT:$FLASK_RUN_PORT -it adi_app /bin/bash
