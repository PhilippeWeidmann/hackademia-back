import weaviate

client = weaviate.Client('http://localhost:8081')

where_filter = {
        "path": ["questionId"],
        "operator": "Equal",
        "valueString": 9
        }

client.query\
        .get("Question", ["questionText", "questionId", "html"])\
        .with_where(where_filter)\
        .do()["data"]["Get"]["Question"]

