import os
import yaml
import logging
from importlib import import_module
from dotenv import load_dotenv
from src.services.document_service import DocumentService
from src.services.ingestion_service import IngestionService

load_dotenv()  # Load environment variables from .env file

def load_plugin(plugin_config_path):
    with open(plugin_config_path, 'r') as file:
        plugin_config = yaml.safe_load(file)
    
    module_name, class_name = plugin_config['module'], plugin_config['class']
    module = import_module(module_name)
    plugin_class = getattr(module, class_name)
    return plugin_class(plugin_config)

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Load the run_analysis configuration
    with open('run_analysis.yaml', 'r') as file:
        config = yaml.safe_load(file)
    
    plugin_configs = config['plugins']
    
    drivers = {}
    config_paths = {}
    for plugin_name, plugin_config_path in plugin_configs.items():
        drivers[plugin_name] = load_plugin(plugin_config_path)
        config_paths[plugin_name] = plugin_config_path
    
    # Initialize the document service with the drivers
    document_service = DocumentService(drivers=drivers, config_paths=config_paths)
    
    # Initialize the ingestion service with the document service
    ingestion_service = IngestionService(document_service=document_service)
    
    # Process all documents
    ingestion_service.process_documents()

if __name__ == "__main__":
    main()
