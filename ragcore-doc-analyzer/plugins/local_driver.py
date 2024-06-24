import os
import logging
from src.drivers.base_driver import BaseDriver

class LocalDriver(BaseDriver):
    def __init__(self, config):
        self.base_path = config['base_path']
        self.permissions = config['permissions']

    def connect(self, **kwargs):
        pass

    def list_files(self, folder_identifier: str):
        full_path = os.path.join(self.base_path, folder_identifier)
        logging.info(f"Listing items in directory: {full_path}")

        files = []
        for root, dirs, items in os.walk(full_path):
            for item in items:
                file_path = os.path.join(root, item)
                relative_path = os.path.relpath(file_path, self.base_path)
                files.append(relative_path)

        logging.info(f"Files found: {files}")
        return files

    def get_file(self, file_identifier: str):
        full_path = os.path.join(self.base_path, file_identifier)
        with open(full_path, 'rb') as file:
            return file.read()
