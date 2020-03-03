#!/bin/bash
for i in `./sqlite3.exe ../lib/db.sqlite .dump | grep 'CREATE' | awk -F '"' '{print $2}'`;
do
    echo $i >> tables.txt
    ./sqlite3.exe ../lib/db.sqlite .dump | grep -A25 'CREATE TABLE IF NOT EXISTS '\"$i\"'' | sed -n -e '/CREATE/,/CREATE/ p' | grep -v 'CREATE\|INSERT\|PRIMARY\|UNIQUE\|);' | awk -F ' ' '{print $1}' | awk '{printf "%s, ",$1}' | head -c -2 >> $i.temp;
    ./sqlite3.exe ../lib/db.sqlite .dump | grep 'INSERT INTO '$i'' | awk -F 'VALUES' '{print $2}' >> $i.temp_sql;
done

sed -i 's|\"||g' *.temp

while read table_name
do
  while read line
    do
           echo "INSERT INTO $table_name (`cat $table_name.temp`) VALUES $line" >> data_temp.sql
        done < "$table_name".temp_sql
done < tables.txt
grep -v 'MEDIA_LIBRARY\|MEDIA_DEFAULT' data_temp.sql > data.sql

rm -rf *temp* *.txt


#If using native sqlite older version, please use the following script
#
#for i in `sqlite3 db.sqlite .dump | grep 'CREATE' | awk -F '"' '{print $2}'`;
#do
#    echo $i >> tables.txt
#        sqlite3 db.sqlite .dump | grep -A25 'CREATE TABLE '\"$i\"'' | grep -v 'CREATE\|INSERT\|PRIMARY\|UNIQUE\|);' | awk -F ' ' '{print $1}' | awk '{printf "%s, ",$1}' | head -c -2 >> $i.temp;
#        sqlite3 db.sqlite .dump | grep 'INSERT INTO '\"$i\"'' | awk -F '"' '{print $3}' >> $i.temp_sql;
#done
#
#sed -i 's|\"||g' *.temp
#
#while read table_name
#do
#  while read line
#    do
#           echo "INSERT INTO $table_name (`cat $table_name.temp`) $line" >> data_temp.sql
#        done < "$table_name".temp_sql
#done < tables.txt
#grep -v 'MEDIA_LIBRARY\|MEDIA_DEFAULT' data_temp.sql > data.sql
#
#rm -rf *temp* *.txt
