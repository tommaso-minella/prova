from pydantic import BaseModel
from typing import List

class UserPermission(BaseModel):
    id: int
    user_email: str
    db_name: str

    class Config:
        orm_mode = True

class UserPermissionsResponse(BaseModel):
    permissions: List[UserPermission]
