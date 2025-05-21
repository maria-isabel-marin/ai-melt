from abc import ABC, abstractmethod

class BaseModel(ABC):
    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def detect_metaphors(self, sentences: list[str]) -> list[dict]:
        pass