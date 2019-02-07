#!/usr/bin/env python3

"""
BASICS

Creates the main API to interact with users directly
"""


import datetime
from flask import Flask, request, jsonify
import os

import finite_difference as fdif
import first_parser as fp
import influx_logger as ilog
import login_action as logac
import mongo_logger as monlog
import pde_parser as pdep


app = Flask(__name__)



@app.route("/zelkova/api/ping", methods=['GET'])
def ping():
    return "pong"



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
    infringent_IP = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    if not logac.validate_user(user, password):  
        ilog.failed_login(infringent_IP, user, "job submission")
        return "INVALID, user is not allowed access"

    # Ensures that x, t variables are provided and correctly formatted
    XT = fp.ensure_time(R["Variables"])
    if not XT:
        return "t variable is not provided"

    # Store basic job information
    JOB_INFO = {}
    JOB_INFO["Solver"] = R["Solver"]
    JOB_INFO["User"] = user
    JOB_INFO["UTC (user submission)"] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")

    # Analyzes the variables and obtains the corresponding type
    JOB_INFO["Constants"] = R["Variables"]
    JOB_INFO["Variables"] = fp.count_xvars(R["Variables"])
    if JOB_INFO["Variables"]["count"] == 0:
        return "INVALID, no main variables were found"

    # Removes all main vars
    for elem in JOB_INFO["Variables"].keys():
        JOB_INFO["Constants"].pop(elem, None)

    JOB_INFO["Time"] = JOB_INFO["Variables"]["t"]
    JOB_INFO["Variables"].pop("t", None)


    # Ensures the existance of the equation and proper syntax
    if not fp.valid_pde_equation(R["Equation"])[0]:
        return fp.valid_pde_equation(R["Equation"])[1] # Error message

    # Ensures that all operations have the correct syntax
    # x, t, u are taking at value 1 (no effect in operation)
    copyvar = dict(R["Variables"])
    if JOB_INFO["Variables"]["count"] == 1:
        # Assumed that the variable is x and the output function is u
        copyvar["x"] = {'value':1}
        copyvar['t'] = {'value':1}
        copyvar['u'] = {'value':1}

    else:
        return "INVALID, one main var is supported at the moment"

    # Ensures that all operations have the correct syntax
    op_count = 0
    for one_operation in R["Equation"]["Right"]:
        # Checks both non-linear and quasilinear operation
        if one_operation["Q-function"] != "None":
            try:
                pdep.correct_argv(one_operation["Q-function"], copyvar)
            except Exception as e:
                return "INVALID, "+str(e)

        if one_operation["NL-function"] != "None":
            try:
                pdep.correct_argv(one_operation["NL-function"], copyvar)
            except Exception as e:
                return "INVALID, "+str(e)

        # Computes PDE coefficients
        if one_operation["partial"] == 0:
            continue

        if one_operation["pvar"] not in JOB_INFO["Variables"].keys():
            return "INVALID, '"+one_operation["pvar"]+"' is not a variable"


        JOB_INFO["op-"+str(op_count)] = one_operation
        JOB_INFO["op-"+str(op_count)]["finite coefficients"] = fdif.finite_difference_coefficients(one_operation["partial"], 
                                one_operation["Accuracy"], JOB_INFO["Variables"][one_operation["pvar"]]["h"])
        op_count += 1

    JOB_INFO["number of operations"] = op_count
    JOB_INFO["Status"] = "Waiting"


    # Adds all the information to MongoDB to be parsed later
    mongo_submit = monlog.new_job(JOB_INFO)
    if not mongo_submit[0]:
        return "INVALID\n"+mongo_submit[1]

    # Adds a record of job started to InfluxDB
    ilog.job_submission(infringent_IP, user, mongo_submit[1], JOB_INFO["Variables"]["count"], op_count)

    return "Your job has been correctly submitted\nJob ID: "+str(mongo_submit[1])



# Returns a list of jobns submitted a user
@app.route("/zelkova/api/jobs/list_ids", methods=['GET'])
def job_list_ids():

    # Requires json
    try:
        R = request.get_json()
    except:
        return "INVALID, json could not be parsed"

    infringent_IP = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    # Ensure the existance of basic keys
    try:
        user = R["user"]
        password = R["password"]
    except:
        ilog.failed_login(infringent_IP, user, "id checks")

    if not logac.validate_user(user, password):  
        ilog.failed_login(infringent_IP, user, "id checks")
        return "INVALID, user is not allowed access"

    return jsonify(monlog.get_all_user_jobs_ids(user))





if __name__ == '__main__':
    app.run()
