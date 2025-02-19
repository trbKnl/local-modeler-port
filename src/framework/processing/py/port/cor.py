""" 
Module to estimate correlation with local modeler
"""

# https://stats.stackexchange.com/questions/410468/online-update-of-pearson-coefficient

import math
import json

from port.api.commands import (
    CommandSystemGetParameters,
    CommandSystemPutParameters,
)

def learn_params(model, x, y):
    if model == None:
        n = sum_x = sum_y = ss_x = ss_y = ss_xy = 0
        model = {
            "n": 0,
            "sum_x": 0,
            "sum_y": 0,
            "ss_x": 0,
            "ss_y": 0,
            "ss_xy": 0
        }
    else:
        model = json.loads(model)

    sum_x = model["sum_x"] = model["sum_x"] + x
    sum_y = model["sum_y"] = model["sum_y"] + y
    ss_x = model["ss_x"] = model["ss_x"] + x**2
    ss_y = model["ss_y"] = model["ss_y"] + y**2
    ss_xy = model["ss_xy"] = model["ss_xy"] + x*y
    n = model["n"] = model["n"] + 1

    try:
        numerator = ss_xy - ((sum_x * sum_y) / n)
        denominator = math.sqrt(ss_x - (sum_x ** 2 / n)) * math.sqrt(ss_y - (sum_y ** 2 / n)) 
        correlation = numerator / denominator
    except Exception as e:
        print(e)
        correlation = float("nan")

    model["correlation"] = correlation
    return json.dumps(model)



def getParameters(study_id):
    return CommandSystemGetParameters(study_id=study_id)


def putParameters(run_json: str, following_count, followers_count, study_id):
    run = json.loads(run_json)

    new_model = learn_params(run["model"], following_count, followers_count)

    return CommandSystemPutParameters(
        id=run["id"],
        model=new_model,
        check_value=run["check_value"],
        study_id=study_id
    )
