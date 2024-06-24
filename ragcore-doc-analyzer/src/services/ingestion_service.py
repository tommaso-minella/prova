import logging
import time
from src.partitioning.partitioning import partition_content
from src.cleaning.cleaning import clean_content
from src.chunking.chunking import chunk_content
from src.embedding.embedding import embed_content
from src.staging.staging import stage_content

class IngestionService:
    def __init__(self, document_service):
        self.document_service = document_service

    def process_documents(self):
        files = self.document_service.list_files()
        logging.info(f"Files to process: {files}")
        for file_identifier in files:
            logging.info(f"Processing document: {file_identifier}")
            users = self.document_service.get_users_with_access(file_identifier)
            logging.info(f"Users: {', '.join(users)}")
            try:
                start_time = time.time()
                blob = self.document_service.get_file(file_identifier)
                partitioned_content = self.partition(blob, file_identifier)
                cleaned_content = self.clean(partitioned_content)
                chunked_content = self.chunk(cleaned_content)
                staged_chunks = self.stage(chunked_content, file_identifier, users)
                embedding_response = self.embed(staged_chunks)
                end_time = time.time()
                logging.info(f"Total time for processing {file_identifier}: {end_time - start_time} seconds")
            except ValueError as e:
                logging.error(f"Error processing {file_identifier}: {e}")

    def partition(self, blob, file_identifier):
        logging.info("Partitioning content")
        start_time = time.time()
        partitioned_content = partition_content(blob, file_identifier)
        end_time = time.time()
        logging.info(f"Time taken for partitioning: {end_time - start_time} seconds")
        return partitioned_content

    def clean(self, partitioned_content):
        logging.info("Cleaning content")
        start_time = time.time()
        cleaned_content = clean_content(partitioned_content)
        end_time = time.time()
        logging.info(f"Time taken for cleaning: {end_time - start_time} seconds")
        return cleaned_content

    def chunk(self, cleaned_content):
        logging.info("Chunking content")
        start_time = time.time()
        chunked_content = chunk_content(cleaned_content)
        end_time = time.time()
        logging.info(f"Time taken for chunking: {end_time - start_time} seconds")
        return chunked_content

    def stage(self, chunked_content, file_identifier, users):
        logging.info("Staging content")
        start_time = time.time()
        staged_content = stage_content(chunked_content, file_identifier, users)
        end_time = time.time()
        logging.info(f"Time taken for staging: {end_time - start_time} seconds")
        return staged_content

    def embed(self, staged_chunks):
        logging.info("Embedding content")
        start_time = time.time()
        embedding_response = embed_content(staged_chunks)
        end_time = time.time()
        logging.info(f"Time taken for embedding: {end_time - start_time} seconds")
        return embedding_response
