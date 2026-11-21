from abc import ABC, abstractmethod
from typing import Any
class Repository(ABC):

    @abstractmethod
    def create(self, data: Any):
        pass
    @abstractmethod
    def findAll(self):
        pass

    @abstractmethod
    def exists(self, params):
        pass

    @abstractmethod
    def findById(self, id):
        pass
    @abstractmethod
    def update(self, id, column: str, data: Any):
        pass

    @abstractmethod
    def delete(self, id):
        pass
