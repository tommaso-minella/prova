from pydantic import BaseModel, Field
from typing import List, Optional
from .message import Message

class Chat(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: str
    session_id: str
    messages: List[Message] = []
    created_at: Optional[str]
    updated_at: Optional[str]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
