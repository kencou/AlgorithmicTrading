from abc import ABC, abstractmethod
from typing import List

class BaseAlgorithm(ABC):
    """Abstract base for all trading Algorithm."""
    def __init__(self):
        pass

    @abstractmethod
    def run(self, prices) -> float:
        pass
