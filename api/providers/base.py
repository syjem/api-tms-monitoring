from abc import ABC, abstractmethod


class BaseProvider(ABC):
    @abstractmethod
    def extract(self, file_bytes: bytes) -> dict:
        pass
