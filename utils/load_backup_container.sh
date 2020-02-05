#!/bin/bash
containerid=$(docker ps | grep adi_explorer | awk -F ' ' '{print $1}')
docker exec -i $containerid sqlite3 /app/lib/db.sqlite < data.sql