"""
BASICS

Parses a user JSON to obtain information about the PDE
"""

import math


# VARIABLES (dict): Variables dictionary

# Checks if a certain word is a variable
def is_variable(VARIABLES, variable):

    try:
        if variable in VARIABLES.keys():
            return True
    except:
        return False
    return False


# Given a JSON set of operations, it returns a list of arrays of all operations, in order
# Designed as a test location, not for actually being run
# Proper operations are run in the containers
# OPERATIONS (dict)
def compute_ops(OPERATIONS, VARIABLES):


    if is_variable(VARIABLES, OPERATIONS):
        return VARIABLES[OPERATIONS]["value"]


    # Checks the number of keys
    if ("op" not in OPERATIONS):
        raise SyntaxError("'op' key not present")
    if ("args" not in OPERATIONS):
        raise SyntaxError("'args' key not present")

    actual_op = OPERATIONS["op"]

    if actual_op == "+":
        OP = 0.00
        if len(OPERATIONS["args"]) < 2:
            raise SyntaxError("'+' operation requires 2 or more elements, "+str(len(OPERATIONS["args"]))+" provided")
        for qq in range(0, len(OPERATIONS["args"])):
            OP += compute_ops(OPERATIONS["args"][qq], VARIABLES)
        return OP


    if actual_op == "-":
        if len(OPERATIONS["args"]) != 2:
            raise SyntaxError("'+' operation requires 2 elements, "+str(len(OPERATIONS["args"]))+" provided")
        return compute_ops(OPERATIONS["args"][0], VARIABLES)-compute_ops(OPERATIONS["args"][1], VARIABLES)

    if actual_op == "*":
        if len(OPERATIONS["args"]) < 2:
            raise SyntaxError("'*' operation requires 2 or more elements, "+str(len(OPERATIONS["args"]))+" provided")

        OP = 1
        for qq in range(0, len(OPERATIONS["args"])):
            OP *= compute_ops(OPERATIONS["args"][qq], VARIABLES)
        return OP        


    if actual_op == "/":
        if len(OPERATIONS["args"]) != 2:
            raise SyntaxError("'/' operation requires 2 elements, "+str(len(OPERATIONS["args"]))+" provided")
        return compute_ops(OPERATIONS["args"][0], VARIABLES)/compute_ops(OPERATIONS["args"][1], VARIABLES)


    if actual_op == "abs":
        if len(OPERATIONS["args"]) != 1:
            raise SyntaxError("'abs' operation requires 1 element, "+str(len(OPERATIONS["args"]))+" provided")        
        return abs(compute_ops(OPERATIONS["args"][0], VARIABLES))


    if actual_op == "root2":
        if len(OPERATIONS["args"]) != 1:
            raise SyntaxError("'root2' operation requires 1 element, "+str(len(OPERATIONS["args"]))+" provided")        
        return math.sqrt(compute_ops(OPERATIONS["args"][0], VARIABLES))


    if actual_op == "**":
        if len(OPERATIONS["args"]) != 2:
            raise SyntaxError("'/' operation requires 2 elements, "+str(len(OPERATIONS["args"]))+" provided")
        return compute_ops(OPERATIONS["args"][0], VARIABLES)**compute_ops(OPERATIONS["args"][1], VARIABLES)


    if actual_op == "root":
        if len(OPERATIONS["args"]) != 2:
            raise SyntaxError("'/' operation requires 2 elements, "+str(len(OPERATIONS["args"]))+" provided")
        return compute_ops(OPERATIONS["args"][0], OP, VARIABLES)**(1/compute_ops(OPERATIONS["args"][0], OP, VARIABLES))


    if actual_op == "log10":
        if len(OPERATIONS["args"]) != 1:
            raise SyntaxError("'/' operation requires 1 element, "+str(len(OPERATIONS["args"]))+" provided")
        return math.log10(compute_ops(OPERATIONS["args"][0], OP, VARIABLES))


    if actual_op == "ln":
        if len(OPERATIONS["args"]) != 1:
            raise SyntaxError("'/' operation requires 1 element, "+str(len(OPERATIONS["args"]))+" provided")
        return math.log(compute_ops(OPERATIONS["args"][0], OP, VARIABLES))


    if actual_op == "log":
        if len(OPERATIONS["args"]) != 2:
            raise SyntaxError("'/' operation requires 2 element, "+str(len(OPERATIONS["args"]))+" provided")
        return math.log(compute_ops(OPERATIONS["args"][1], VARIABLES), compute_ops(OPERATIONS["args"][0], VARIABLES))

    return OP




# Functions and their arguments
FUNC_ARGS = {"+":-1, "-":2, "*":-1, "/":2, "abs":1, "**":2, "root2":1, "root":2, "log": 2, "ln":1, "log10":1}


# Ensures that all functions have the correct number of arguments
def correct_argv(OPERATIONS, VARIABLES):

    if is_variable(VARIABLES, OPERATIONS):
        return 1


    # Checks the number of keys
    if ("op" not in OPERATIONS):
        raise SyntaxError("'op' key not present")
    if ("args" not in OPERATIONS):
        raise SyntaxError("'args' key not present")


    if OPERATIONS["op"] not in FUNC_ARGS.keys():
        raise SyntaxError("Operation '"+OPERATIONS["op"]+"' is not a permitted operation")


    # Operations with unlimited numbers
    if (FUNC_ARGS[OPERATIONS["op"]] == -1):
        if len(OPERATIONS["args"]) > 1:
            OP = 1 
            for qq in range(0, len(OPERATIONS["args"])):
                OP *= correct_argv(OPERATIONS["args"][qq], VARIABLES)
            return OP
        else:
            raise SyntaxError("'"+OPERATIONS["op"]+"' operation require >= 2 inputs, "+str(len(OPERATIONS["args"]))+" were provided")




    else:
        if (len(OPERATIONS["args"]) != FUNC_ARGS[OPERATIONS["op"]]):
            raise SyntaxError("'"+OPERATIONS["op"]+"' operation requires "+str(FUNC_ARGS[OPERATIONS["op"]])+" elements, "+str(len(OPERATIONS["args"]))+" provided")
        # Operation has the correct number of arguments, checks its
        OP = 1 
        for qq in range(0, len(OPERATIONS["args"])):
            OP *= correct_argv(OPERATIONS["args"][qq], VARIABLES)

        return OP


