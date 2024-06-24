from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal, engine, Base
from src import crud
from src.schemas.query import QueryRequest, QueryResponse
from src.models.permission import VectorDbPermission
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#TODO POST embed

@app.post("/query/", response_model=QueryResponse)
async def query_vectordb(request: QueryRequest, db: Session = Depends(get_db)):
    try:
        user_permissions = crud.get_user_permissions(db, request.user_email)
        if not user_permissions:
            raise HTTPException(status_code=403, detail="Access forbidden")

        result = crud.query_vector_db(request.query, user_permissions)
        combined_answer = " ".join([res.page_content for res in result])  # Combine all page contents into a single string
        return QueryResponse(answer=combined_answer, source_documents=[res.metadata for res in result])
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/list_databases/")
async def list_databases(user_email: str, db: Session = Depends(get_db)):
    try:
        user_permissions = crud.get_user_permissions(db, user_email)
        return {"databases": user_permissions}
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
