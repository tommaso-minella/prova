import os
import time
import psycopg2
from langchain_postgres import PGVector
from langchain_core.documents import Document
from langchain_openai import AzureOpenAIEmbeddings

# Function to initialize vector store
def initialize_vector_db(db_name, table_name, pdf_folder_path):
    conn = None
    try:
        conn = psycopg2.connect(os.getenv("POSTGRES_VECTORDB_CONNECTION_STRING"))
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}';")
        exists = cursor.fetchone()
        if not exists:
            print(f"Creating db {db_name}")
            cursor.execute(f"CREATE DATABASE {db_name};")
        
        cursor.close()
        conn.close()
        
        connection_string = f"{os.getenv('POSTGRES_VECTORDB_CONNECTION_STRING')}/{db_name}"
        conn = psycopg2.connect(connection_string)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            content JSONB,
            metadata JSONB
        );""")
        
        # Ensure the table is present before proceeding
        table_exists = False
        retries = 5
        while retries > 0 and not table_exists:
            cursor.execute(f"SELECT to_regclass('{table_name}');")
            if cursor.fetchone()[0] is not None:
                table_exists = True
            else:
                retries -= 1
                time.sleep(2)  # Wait for 2 seconds before retrying
        
        if not table_exists:
            raise Exception(f"Table {table_name} was not created successfully in database {db_name}.")
        
        cursor.close()
        conn.close()
        
        embeddings = AzureOpenAIEmbeddings(
            azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME"),
            openai_api_version=os.getenv("AZURE_OPENAI_EMBEDDINGS_API_VERSION")
        )
        
        vectorstore = PGVector(
            embeddings=embeddings,
            collection_name=table_name,
            connection=connection_string,
            use_jsonb=True,
        )
        
        docs = []
        for pdf_file in os.listdir(pdf_folder_path):
            if pdf_file.endswith(".pdf"):
                with open(os.path.join(pdf_folder_path, pdf_file), "rb") as f:
                    content = f.read()
                    document_content = content.decode('latin-1')
                    print(f"Adding document from {pdf_file}:")
                    print(document_content[:500])  # Print first 500 characters for verification
                    docs.append(Document(page_content=document_content, metadata={"source": pdf_file}))
        
        vectorstore.add_documents(docs)
        print(f"Initialized vector store for {db_name} with documents from {pdf_folder_path}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

# Initialize databases
db_name_1 = "vectordb1"
table_name_1 = "documents"
db_name_2 = "vectordb2"
table_name_2 = "documents"

initialize_vector_db(db_name_1, table_name_1, "./data/pdf1")
initialize_vector_db(db_name_2, table_name_2, "./data/pdf2")

print("Initialization complete.")
