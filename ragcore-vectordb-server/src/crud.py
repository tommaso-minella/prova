from sqlalchemy.orm import Session
from src.models.permission import VectorDbPermission
from src.models.query import QueryResult
from src.schemas.query import QueryResponse
from langchain_postgres import PGVector
from langchain_openai import AzureOpenAIEmbeddings
import os

# Configure Azure OpenAI embeddings
embeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME"),
    openai_api_version=os.getenv("AZURE_OPENAI_EMBEDDINGS_API_VERSION")
)

def get_user_permissions(db: Session, user_email: str):
    permissions = db.query(VectorDbPermission).filter(VectorDbPermission.user_email == user_email).all()
    return [permission.db_name for permission in permissions]

def query_vector_db(query: str, db_names: list) -> QueryResult:
    combined_results = []

    for db_name in db_names:
        connection_string = os.getenv("POSTGRES_VECTORDB_CONNECTION_STRING")
        vectorstore = PGVector(
            embeddings=embeddings,
            collection_name=db_name,
            connection=connection_string,
            use_jsonb=True,
        )

        results = vectorstore.similarity_search(query, k=10)
        combined_results.extend(results)

    return combined_results

def list_user_databases(db: Session, user_email: str) -> list:
    permissions = get_user_permissions(db, user_email)
    return permissions
