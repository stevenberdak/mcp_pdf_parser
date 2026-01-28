from pydantic import BaseModel
from typing import List, Literal

class Answer(BaseModel):
    action: Literal["answer"] = "answer"
    answer: str
    citations: List[str]
