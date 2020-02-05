#!/bin/bash
sqlite3 ../lib/db.sqlite .schema > schema.sql
sqlite3 ../lib/db.sqlite .dump > dump.sql
grep -vx -f schema.sql dump.sql > data.temp
grep -v 'MEDIA_LIBRARY' data.temp > data1.temp
grep -v 'MEDIA_DEFAULT' data1.temp > data.sql
rm -rf schema.sql dump.sql *.temp