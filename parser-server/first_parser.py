"""
BASICS

Ensures the existance and correct location of keys
"""


# Ensures the existance of the main keys
# COMPLETE (large dict): Complete JSON directory with all tags and subtags
def ensure_main_keys(COMPLETE):

    K = COMPLETE.keys()

    if {"user", "password", "Solver", "Variables", "Equation", "Initial Conditions", "Boundary Conditions"}.issubset(set(K)):
        return True

    return False


# Returns a string with missing variables
def keys_missing(COMPLETE):
    PROVIDED = COMPLETE.keys()
    EXPECTED = {"user", "password", "Solver", "Variables", "Equation", "Initial Conditions", "Boundary Conditions"}

    missing = []

    for exp in EXPECTED:
        if exp not in PROVIDED:
            missing.append(exp)

    return "Missing keys: "+",".join(missing)


# Ensures the existance of the main variables
# VARIABLES (dict): Variables dictionary
def ensure_time(VARIABLES):

    K = VARIABLES.keys()

    if "t" not in K:
        return False

    if ("min" not in VARIABLES["t"].keys()) or ("max" not in VARIABLES["t"].keys()) or ("min" not in VARIABLES["k"].keys()):
        return False

    return True


# Returns the number of main variables:
# Return [count, [min, max, h], [...], ...]
def count_xvars(VARIABLES):

    tvar = VARIABLES.keys()
    info = {"count":0}

    for var in tvar:
        if VARIABLES[var]["type"] == "main":
            info["count"] += 1
            info[var] = VARIABLES[var]

    info["time"] = VARIABLES["t"]

    return info


# Ensures basic equation properties
def valid_pde_equation(EQUATION):
    try:
        left, right = EQUATION["Left"], EQUATION["Right"]
    except:
        return [False, "Equation must contain Left, Right keys"]

    # Left side can only be du/dt
    if left != {"t-derivatives":1}:
        return [False, "Left side must be only du/dt: \"Left\":{\"t-derivatives\":1}"]


    # Requires the existance of at least one key
    

