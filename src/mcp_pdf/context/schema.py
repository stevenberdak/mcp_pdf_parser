from dataclasses import dataclass
from typing import List

@dataclass
class RetrievedChunk:
    chunk_id: str
    text: str
    source: str
    page: int
    score: float

@dataclass
class ModelContext:
    query: str
    retrieved: List[RetrievedChunk]
    metadata: dict
