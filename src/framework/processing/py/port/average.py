"""
Module to estimate the average with local modeler
"""

import json

from port.api.commands import (
    CommandSystemGetParameters,
    CommandSystemPutParameters,
)

STUDY_ID="average"

def learn_params(number_of_likes: int, model: str | None) -> str:
    if model is None:
        new_model = {
            "average": number_of_likes,
            "n": 1
        }
    else:
        loaded_model: dict[str, float] = json.loads(model)
        new_n = loaded_model["n"] + 1
        new_average = (loaded_model["average"] * loaded_model["n"] + number_of_likes) / new_n

        new_model = {
            "average": new_average,
            "n": new_n
        }

    return json.dumps(new_model)


def getParameters(study_id=STUDY_ID):
    return CommandSystemGetParameters(study_id=study_id)

def putParameters(run_json: str, data):
    run = json.loads(run_json)
    new_model = learn_params(data, run["model"])
    return CommandSystemPutParameters(
        id=run["id"],
        model=new_model,
        check_value=run["check_value"],
        study_id=STUDY_ID
    )
