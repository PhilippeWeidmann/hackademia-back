from typing import Optional, List
from pydantic import BaseModel

class Answer(BaseModel):
    answerText: str
    vector: Optional[list[int]] = None
    ratings: Optional[list[int]] = None

class Question(BaseModel):
    questionId: str
    questionText: str

class TreeNode(BaseModel):
    parent: str
    child: int
    lambda_val: float
    child_size: int
    answerText: Optional[str]
    originalAnswerId: Optional[int]
    ratings: Optional[List[int]]