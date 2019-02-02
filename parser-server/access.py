#!/usr/bin/env python3

"""
BASICS

Creates the main API to interact with users directly
"""


import datetime
import finite_difference as fdif
import first_parser as fp
from flask import Flask, request
import login_action as logac
import os
import pde_parser as pdep
import uuid


app = Flask(__name__)




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
    JOB_INFO["Constants"] = R["Variables"]
    JOB_INFO["Variables"] = fp.count_xvars(R["Variables"])
    if JOB_INFO["Variables"]["count"] == 0:
        return "INVALID, no main variables were found"

    # Removes all main vars
    for elem in JOB_INFO["Variables"].keys():
        JOB_INFO["Constants"].pop(elem, None)

    JOB_INFO["Time"] = JOB_INFO["Variables"]["t"]
    JOB_INFO["Variables"].pop("t", None)

    # Obtains the number of desired nodes (3 if never specified)
    user_max_nodes = logac.max_request_nodes(user)
    if user_max_nodes == 0:
        return "INVALID, user is not allowed access to nodes"

    user_requested_nodes = R["requested-nodes"]

    if user_requested_nodes > user_max_nodes:
        user_requested_nodes = user_max_nodes

    JOB_INFO["requested-nodes"] = user_requested_nodes

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
    JOB_INFO["id"] = str(uuid.uuid4())




    # Adds all the information to ElasticSearch to be parsed later





    # Adds a record of job started to InfluxDB




    return "Test passed"













if __name__ == '__main__':
    app.run()
