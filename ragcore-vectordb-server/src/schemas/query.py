from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    user_email: str
    query: str

class QueryResponse(BaseModel):
    answer: str
    source_documents: List[str]