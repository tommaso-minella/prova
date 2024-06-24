# src/drivers/base_driver.py
from abc import ABC, abstractmethod

class BaseDriver(ABC):
    @abstractmethod
    def connect(self, **kwargs):
        pass

    @abstractmethod
    def list_files(self, folder_path: str):
        pass

    @abstractmethod
    def get_file(self, file_identifier: str):
        pass
