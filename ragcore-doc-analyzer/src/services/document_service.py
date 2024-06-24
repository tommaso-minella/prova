import os
import yaml
import logging
from src.drivers.base_driver import BaseDriver

class DocumentService:
    def __init__(self, drivers: dict, config_paths: dict):
        self.drivers = drivers
        self.configs = {}
        for plugin, config_path in config_paths.items():
            with open(config_path, 'r') as file:
                self.configs[plugin] = yaml.safe_load(file)

    def list_files(self):
        all_files = []
        for plugin, driver in self.drivers.items():
            files = driver.list_files('')
            logging.info(f"Files from plugin {plugin}: {files}")
            prefixed_files = [f"{plugin}::{file}" for file in files]
            all_files.extend(prefixed_files)
        logging.info(f"All files: {all_files}")
        return all_files

    def get_file(self, file_identifier: str):
        plugin, identifier = file_identifier.split("::", 1)
        driver = self.drivers[plugin]
        file_blob = driver.get_file(identifier)
        return file_blob
    
    def get_users_with_access(self, file_identifier: str):
        plugin, identifier = file_identifier.split("::", 1)
        permissions = self.configs[plugin]['permissions']
        if identifier in permissions['files']:
            allowed_users = set(permissions['files'][identifier].get('users', []))
            allowed_groups = permissions['files'][identifier].get('groups', [])
        else:
            parent_identifier = os.path.dirname(identifier)
            if parent_identifier in permissions['folders']:
                allowed_users = set(permissions['folders'][parent_identifier].get('users', []))
                allowed_groups = permissions['folders'][parent_identifier].get('groups', [])
            else:
                allowed_users = set()
                allowed_groups = []

        for group in allowed_groups:
            group_members = permissions['groups'].get(group, [])
            allowed_users.update(group_members)
        
        return list(allowed_users)
