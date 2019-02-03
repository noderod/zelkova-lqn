"""
BASICS

Stores API log information in InfluxDB
"""


import datetime
from influxdb import InfluxDBClient
import os




# Returns a string in UTC time in the format YYYY-MM-DD HH:MM:SS.XXXXXX (where XXXXXX are microseconds)
def timformat():
    return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")


# Logs a failed login
# IP (str): IP used
# unam (str): username used
# action (str)
# due_to (str): Reason for failed login, most likely due to incorrect key

def failed_login(IP, unam, action, due_to="incorrect_key"):
    FC = InfluxDBClient(host = os.environ['URL_BASE'], port = 8086, username = os.environ['INFLUXDB_WRITE_USER'], 
        password = os.environ['INFLUXDB_WRITE_USER_PASSWORD'], database = 'failed_login')

    FC.write_points([{
                    "measurement":"bad_credentials",
                    "tags":{
                            "id":unam,
                            "action":action,
                            "reason":due_to
                            },
                    "time":timformat(),
                    "fields":{
                            "client-IP":IP
                            }
                    }])



# User does not have access to nodes
def failed_node_request(IP, unam, action="node request", due_to="node access not allowed"):
    FC = InfluxDBClient(host = os.environ['URL_BASE'], port = 8086, username = os.environ['INFLUXDB_WRITE_USER'], 
        password = os.environ['INFLUXDB_WRITE_USER_PASSWORD'], database = 'failed_login')

    FC.write_points([{
                    "measurement":"bad_node_requests",
                    "tags":{
                            "id":unam,
                            "action":action,
                            "reason":due_to
                            },
                    "time":timformat(),
                    "fields":{
                            "client-IP":IP
                            }
                    }])
