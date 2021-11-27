from typing import List
from fastapi import FastAPI
from db.answers import get_tree, TreeNode
import weaviate
from models.models import Answer, Question
import redis
import pickle
import os

redis = redis.Redis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'])

# or another location where your Weaviate instance is running
client = weaviate.Client(os.environ['WEAVIATE_URL'])

app = FastAPI()

@app.get('/question/{questionRef}/answers', response_model=List[TreeNode])
def get_answer_tree(questionRef: str) -> List[TreeNode]:
    '''
    Returns the answers grouped semantically and hierarchically in the form of a json tree
    '''
    if redis.get(questionRef):
        return pickle.loads(redis.get(questionRef))
    else:
        tree = get_tree(questionRef)
        redis.set(questionRef, pickle.dumps(tree))
        return tree


@app.put('/question/{questionRef}/answers', response_model=str)
def add_answer(questionRef: str, answer: Answer) -> str:
    '''
    Returns the UUID of the created answer
    '''
    return client.data_object\
        .create(
            data_object=answer.dict() + {'questionId': questionRef},
            class_name="Answer")


@app.post('/questions', response_model=List[Question])
def get_questions_near_terms(search_terms) -> List[Question]:
    print(search_terms)
    near_text_filter = {
        "concepts": search_terms,
        "certainty": 0.7
    }
    # TODO: Implement USE embedding and use near_vector search...

    return client.query\
        .get("Question", ["questionText", "questionId", "html"])\
        .with_near_text(near_text_filter)\
        .do()["data"]["Get"]["Question"]


@app.get('/questions', response_model=List[Question])
def get_questions() -> List[Question]:
    return client.query\
        .get("Question", ["questionText", "questionId", "html"])\
        .do()["data"]["Get"]["Question"]
