import weaviate

client = weaviate.Client('http://glossastra.unige.ch:8081')

def get_question_by_id(questionID: int):
    where_filter = {
        "path": ["questionId"],
        "operator": "Equal",
        "valueNumber": questionID
        }

    return client.query\
        .get("Question", ["questionText", "questionId", "html"])\
        .with_where(where_filter)\
        .do()["data"]["Get"]["Question"]


obj = get_question_by_id(7)
print(type(obj))

