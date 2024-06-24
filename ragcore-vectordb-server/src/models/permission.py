from sqlalchemy import Column, Integer, String
from src.database import Base

class VectorDbPermission(Base):
    __tablename__ = "vector_db_permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    db_name = Column(String, index=True)
