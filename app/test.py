import weaviate
#from models.models import Question

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
        .do()["data"]["Get"]["Question"][0] #take first occurence in case of duplicata



# def add_question(question: Question) -> str:
#     '''
#     Returns the UUID of the created question
#     '''
#     return client.data_object\
#         .create(
#             data_object=question.dict() + {'questionId': question.questionId, 'questionText': question.questionText},
#             class_name="Question")


obj = get_question_by_id(9)
print(obj)
