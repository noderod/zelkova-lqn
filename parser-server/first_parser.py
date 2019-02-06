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

    tkeys = VARIABLES["t"].keys()

    if ("min" not in tkeys) or ("max" not in tkeys) or ("min" not in tkeys) or ("k" not in tkeys):
        return False

    return True



# Returns the number of main variables:
# Return [count, {}, {}, {}]
def count_xvars(VARIABLES):

    tvar = VARIABLES.keys()
    info = {"count":0}

    for var in tvar:
        if VARIABLES[var]["type"] == "main":
            varkeys = VARIABLES[var].keys()
            if ("min" not in varkeys) or ("max" not in varkeys) or ("min" not in varkeys) or ("h" not in varkeys):
                # Lacking information
                return {"count":0}


            info["count"] += 1
            info[var] = VARIABLES[var]

    info["t"] = VARIABLES["t"]

    return info



# Ensures that a dict containing an operation holds sufficient information
def operation_presyntax(opdict):

    # Functions using just the function without any derivatives
    reqkeys = ["Q-function", "NL-function", "partial", "Accuracy", "pvar"]

    if not all(rk in opdict.keys() for rk in reqkeys):
        return False
    return True



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
    if not all(type(rel) is dict for rel in right):
        return [False, "Right side must be an array of operations"]

    for rl in right:
        if not operation_presyntax(rl):
            return [False, "One or more operations do not have the correct syntax"]

    return [True]

