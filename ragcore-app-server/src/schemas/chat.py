from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from .message import Message

class ChatBase(BaseModel):
    user_id: str
    session_id: str

class ChatCreate(ChatBase):
    pass

class Chat(ChatBase):
    id: Optional[str] = Field(alias="_id")
    messages: List[Message] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
