"""
Module to estimate OLS with autograd for local modeler
"""

import numpy as np
import autograd.numpy as anp
from autograd import grad
import pandas as pd
import json

from port.api.commands import (
    CommandSystemGetParameters,
    CommandSystemPutParameters,
)

def linear_model(params: anp.ndarray, x: anp.ndarray) -> anp.ndarray:
    return anp.dot(x, params)

def mse_loss(params: anp.ndarray, x: anp.ndarray, y: anp.ndarray) -> float:
    predictions = linear_model(params, x)
    return anp.mean((predictions - y) ** 2)

gradient = grad(mse_loss)


# Stochastic Gradient Descent function
def sgd(x: np.ndarray, y: np.ndarray, params: np.ndarray, lr: float = 0.01, epochs: int = 100, batch_size: int = 32) -> np.ndarray:
    n_samples, _ = x.shape

    for epoch in range(epochs):
        # Shuffle the dataset
        indices = np.arange(n_samples)
        np.random.shuffle(indices)
        x_shuffled = x[indices]
        y_shuffled = y[indices]
        
        # Iterate over batches
        for i in range(0, n_samples, batch_size):
            x_batch = x_shuffled[i:i + batch_size]
            y_batch = y_shuffled[i:i + batch_size]
            
            # Compute the gradient for the current batch
            grads = gradient(params, x_batch, y_batch)
            
            # Update parameters
            params -= lr * grads
        
        # Optionally print the loss to track the training progress
        loss = mse_loss(params, x, y)
        print(f"Epoch {epoch+1}, Loss: {loss}")
    
    return params


def learn_params(model: str | None, df: pd.DataFrame, x_colnames: list[str], y_colname: str) -> str:
    # test_conditions_about_data(df)
    # if conditions fail do something

    # if not initialized initialize parameters
    if model == None:
        current_params = [0 for _ in range(0, len(x_colnames))]
    else:
        current_params = json.loads(model)

    # convert to x and y
    x =  df.loc[:, x_colnames].values
    y =  df.loc[:, y_colname].values
    params_array = np.array(current_params, dtype=np.float64)

    learned_params_sgd = sgd(x, y, params_array, lr=0.1, epochs=50, batch_size=len(x))
    new_params = json.dumps(learned_params_sgd.tolist())
    return new_params
    

def generate_simple_model_data():
    X1 = np.random.random()
    X2 = np.random.random()
    X3 = np.random.random()
    noise = np.random.normal(0, 0.1)
    Y = 2 * X1 + 3 * X2 - X3 + noise
    df = pd.DataFrame([[X1, X2, X3, Y]], columns=["X1", "X2", "X3", "Y"]) #pyright: ignore
    return df


STUDY_ID="regression"

def getParameters(study_id=STUDY_ID):
    return CommandSystemGetParameters(study_id=study_id)


def putParameters(run_json: str):
    run = json.loads(run_json)

    # generate some fake data
    df = generate_simple_model_data()
    new_model = learn_params(run["model"], df, x_colnames=["X1", "X2", "X3"], y_colname="Y")

    return CommandSystemPutParameters(
        id=run["id"],
        model=new_model,
        check_value=run["check_value"],
        study_id=STUDY_ID
    )
