#!/bin/bash

# Creates the databases:
#  | -api_jobs:  Contains all API job submission data
#  | -failed_login: Incorrect user credentials or user is not authorized


curl -XPOST -u $INFLUXDB_ADMIN_USER:$INFLUXDB_ADMIN_PASSWORD  http://$URL_BASE:8086/query --data-urlencode 'q=CREATE DATABASE "api_jobs"'
curl -XPOST -u $INFLUXDB_ADMIN_USER:$INFLUXDB_ADMIN_PASSWORD  http://$URL_BASE:8086/query --data-urlencode 'q=CREATE DATABASE "failed_login"'
printf "Created InfluxDB databases\n"

# Assigns write privileges
curl -XPOST -u $INFLUXDB_ADMIN_USER:$INFLUXDB_ADMIN_PASSWORD  http://$URL_BASE:8086/query \
    --data-urlencode "q=GRANT WRITE ON \"api_jobs\" TO \"$INFLUXDB_WRITE_USER\""
curl -XPOST -u $INFLUXDB_ADMIN_USER:$INFLUXDB_ADMIN_PASSWORD  http://$URL_BASE:8086/query \
    --data-urlencode "q=GRANT WRITE ON \"failed_login\" TO \"$INFLUXDB_WRITE_USER\""

# Assigns read privileges
curl -XPOST -u $INFLUXDB_ADMIN_USER:$INFLUXDB_ADMIN_PASSWORD  http://$URL_BASE:8086/query \
    --data-urlencode "q=GRANT READ ON \"api_jobs\" TO \"$INFLUXDB_READ_USER\""

# False logins remain an admin priviledge

printf "Database privileges have been added\n"


gunicorn -w $GTH -b $URL_BASE:7500 access:app &
tail -F anything
