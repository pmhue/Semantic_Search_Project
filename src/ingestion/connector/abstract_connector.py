from abc import ABC, abstractmethod
from typing import Iterator

from src.model import Document


class Connector(ABC):
    @abstractmethod
    def load_data(self) -> Iterator[Document]:
        pass
