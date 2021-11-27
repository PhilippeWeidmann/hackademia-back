import os
import pandas as pd
import hdbscan
import umap
import weaviate
from typing import List
from models.models import Answer, TreeNode


# or another location where your Weaviate instance is running
client = weaviate.Client(os.environ["WEAVIATE_URL"])


def get_answers(questionRef: str) -> List[Answer]:
    where_filter = {
        "path": ["question"],
        "operator": "Equal",
        "valueString": questionRef
    }

    query_result = client.query\
        .get("Answer", ["answerText", "originalAnswerId", "ratings"])\
        .with_where(where_filter)\
        .with_additional(["vector"])\
        .do()

    df = pd.json_normalize(query_result["data"]["Get"]["Answer"])

    return df.to_dict()


def get_tree(questionRef: str) -> List[TreeNode]:
    where_filter = {
        "path": ["question"],
        "operator": "Equal",
        "valueString": questionRef
    }

    query_result = client.query\
        .get("Answer", ["answerText", "originalAnswerId", "ratings"])\
        .with_where(where_filter)\
        .with_additional(["vector"])\
        .do()

    df = pd.json_normalize(query_result["data"]["Get"]["Answer"])

    # print(df)

    clusterable_embedding = umap.UMAP(
        n_neighbors=30,
        min_dist=0.0,
        n_components=2,
        random_state=42,
    ).fit_transform(pd.DataFrame(df["_additional.vector"].to_list()))

    clusterer = hdbscan.HDBSCAN()

    # print(df)

    clusterer.fit(clusterable_embedding)

    # # Most data in the 512 point array cannot be clustered so attempt dimensionality reduction first... to avoid getting as many "-1" values for labels
    # print(clusterer.labels_)
    
    return [{
        "parent": "",
        "child": len(query_result["data"]["Get"]["Answer"]),
        "lambda_val": 0,
        "child_size": len(query_result["data"]["Get"]["Answer"])}] + [
            x | (query_result["data"]["Get"]["Answer"][x['child']] if x['child'] < len(query_result["data"]["Get"]["Answer"]) else {}) for x in clusterer.condensed_tree_.to_pandas().to_dict(orient='records')
    ]


# def convert_keys_recursive(d: dict) -> dict:
#     new_d = {}
#     for k, v in d.items():
#         if isinstance(v, dict):
#             new_d[int(k)] = convert_keys_recursive(v)
#         else:
#             if not isinstance(k, str):
#                 new_d[int(k)] = v
#             else:
#                 new_d[k] = v

#     return new_d
