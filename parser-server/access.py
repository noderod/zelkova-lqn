#!/usr/bin/env python3

"""
BASICS

Creates the main API to interact with users directly
"""


import datetime
import first_parser as fp
from flask import Flask, request
import login_action as logac
import os
import pde_parser as pdep
import redis
import uuid


app = Flask(__name__)
r_temp_jobs = redis.Redis(host=os.environ['URL_BASE'], password=os.environ['REDIS_AUTH'], db=3)



@app.route("/zelkova/api/jobs/submit", methods=['POST'])
def submit_job():

    # Requires json
    try:
        R = request.get_json()
    except:
        return "INVALID, json could not be parsed"

    # Ensure the existance of basic keys
    if not fp.ensure_main_keys(R):
        return fp.keys_missing(R)

    user = R["user"]
    password = R["password"]
    if not logac.validate_user(user, password):
        return "INVALID, user is not allowed access"

    # Ensures that x, t variables are provided and correctly formatted
    XT = fp.ensure_time(R["Variables"])
    if not XT:
        return "t variable is not provided"

    # Store basic job information
    JOB_INFO = {}
    JOB_INFO["Solver"] = R["Solver"]
    JOB_INFO["User"] = R["user"]
    JOB_INFO["UTC (user submission)"] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

    # Analyzes the variables and obtains the corresponding type
    main_var_info = fp.count_xvars(R["Variables"])
    if main_var_info["count"] == 0:
        return "INVALID, no main variables were found"

    # Obtains the number of desired nodes (3 if never specified)
    user_max_nodes = logac.max_request_nodes(user)
    if user_max_nodes == 0:
        return "INVALID, user is not allowed access to nodes"

    if "requested-nodes" in R.keys:
        user_requested_nodes = R["nodes"]
    else:
        user_requested_nodes = 3

    if user_requested_nodes > user_max_nodes:
        user_requested_nodes = user_max_nodes

    JOB_INFO["requested-nodes"] = user_requested_nodes

    # Ensures the existance of the equation and proper syntax
    if not fp.valid_pde_equation(R["Equation"])[0]:
        return fp.valid_pde_equation(R["Equation"])[1] # Error message


    # Ensures the type of partial with respect to time is acceptable (du/dt, known as simple)





    # Computes PDE coefficients






    # Adds all the information to Redis to be parsed later





    # Adds a record of job started to InfluxDB
















if __name__ == '__main__':
    app.run()
