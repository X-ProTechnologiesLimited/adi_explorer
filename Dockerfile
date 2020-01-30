FROM python:3.7-alpine
WORKDIR /app

COPY requirements.txt /app/
COPY utils /app/utils/
COPY initialise_db.py /app/
COPY templates/ /app/templates/
COPY lib /app/lib
COPY supp_files /app/supp_files

ENV CONTAINERISED true

USER root
RUN apk add --update python3
RUN apk add --no-cache bash
RUN apk add sqlite
RUN apk add --no-cache curl python3 pkgconfig python3-dev openssl-dev libffi-dev musl-dev make gcc
RUN pip3 install --upgrade pip setuptools
RUN pip3 install -r requirements.txt
RUN if [ -d "lib/__pycache__/" ] ; then rm -rf lib/__pycache__ ; fi
RUN if [ -d "tests/__pycache__/" ] ; then rm -rf tests/__pycache__ ; fi
RUN if [ -d "tests/test_output" ] ; then rm -f tests/test_output/* ; fi
USER root
RUN /bin/sh

ENTRYPOINT ["utils/start_app.sh"]

