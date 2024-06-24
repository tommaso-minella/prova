from pydantic import BaseModel
from typing import List

class QueryResult(BaseModel):
    answer: str
    source_documents: List[str]