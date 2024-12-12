"""
Module to estimate with LDA for local modeler
"""

import json

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np


from port.api.commands import (
    CommandSystemGetParameters,
    CommandSystemPutParameters,
)


def serialize_random_state(rs: np.random.RandomState) -> str:
    """
    Serializes np.random.RandomState to a json string
    """
    state = rs.get_state()
    # tolist if item is ndarray
    serializable_state = [item.tolist() if isinstance(item, np.ndarray) else item for item in state]
    return json.dumps(serializable_state)



def deserialize_random_state(serialized_state: str) -> np.random.RandomState:
    """
    Deserializes a json string containing a random state and returns np.random.RandomState object
    """
    deserialized_state = tuple(
        np.array(item, dtype=np.uint32) if isinstance(item, list) 
        else item 
        for item in json.loads(serialized_state)
    )
    rs = np.random.RandomState()
    rs.set_state(deserialized_state) #pyright: ignore
    return rs


def save_lda_model(lda: LatentDirichletAllocation) -> str:
    model_params = {
        'components_': lda.components_.tolist(),
        'exp_dirichlet_component_': lda.exp_dirichlet_component_.tolist(),
        'doc_topic_prior_': lda.doc_topic_prior_,
        'n_components': lda.n_components,
        'learning_decay': lda.learning_decay,
        'learning_offset': lda.learning_offset,
        'max_iter': lda.max_iter,
        'random_state': lda.random_state,
        'n_batch_iter_': lda.n_batch_iter_,
        'topic_word_prior_': lda.topic_word_prior_,
    }
    model = {
        "model_params": model_params,
        "random_state": serialize_random_state(lda.random_state_)
    }
    return json.dumps(model)


def load_lda_model(serialized_model: str | None, n_components: int) -> LatentDirichletAllocation:
    if serialized_model == None:
        lda = LatentDirichletAllocation(n_components=n_components, learning_method='online', max_iter=1)
        return lda

    model: dict = json.loads(serialized_model)
    model_params = model['model_params']
    random_state = model['random_state']
    
    lda = LatentDirichletAllocation(
        learning_method='online',
        n_components=model_params['n_components'],
        learning_decay=model_params['learning_decay'],
        learning_offset=model_params['learning_offset'],
        max_iter=model_params['max_iter'],
        random_state=model_params['random_state']
    )

    lda.components_ = np.array(model_params['components_'])
    lda.exp_dirichlet_component_ = np.array(model_params['exp_dirichlet_component_'])
    lda.doc_topic_prior_ = model_params['doc_topic_prior_']
    lda.n_batch_iter_ = model_params['n_batch_iter_'] 
    lda.topic_word_prior_ = model_params['topic_word_prior_'] 

    lda.random_state_ = deserialize_random_state(random_state)
    return lda


#def learn_params(data, vocabulary, model: str, n_components) -> str:
def learn_params(data, model: str, n_components) -> str:
    # IMPLEMENT THIS !!!
    # TODO: check conditions of data

    lda = load_lda_model(model, n_components)

    vocabulary = {'a': 0, 'b': 1, 'c': 2, 'third': 3, 'second': 4, 'batch': 5, 'asd': 6}
    vectorizer = CountVectorizer(vocabulary=vocabulary)

    # data should be list of a list of strings
    batch_term_matrix = vectorizer.fit_transform(data)
    lda.partial_fit(batch_term_matrix)
    new_model = save_lda_model(lda)

    return new_model


STUDY_ID="test"

def getParameters(study_id=STUDY_ID):
    return CommandSystemGetParameters(study_id=study_id)


def putParameters(run_json: str, data):
    run = json.loads(run_json)
    new_model = learn_params(data, run["model"], n_components=3)

    return CommandSystemPutParameters(
        id=run["id"],
        model=new_model,
        check_value=run["check_value"],
        study_id=STUDY_ID,
    )

